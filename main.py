from flask import Flask, render_template, request, jsonify
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
import re
import os
import resource

# Disable Flask's file system monitoring before creating the app
os.environ['FLASK_DISABLE_FILE_WATCHERS'] = '1'

app = Flask(__name__)

# Initialize Qdrant client configuration
QDRANT_HOST = os.getenv('QDRANT_HOST', 'localhost')
QDRANT_PORT = int(os.getenv('QDRANT_PORT', '6333'))
collection_name = "animal_collection"

# Lazy initialization of Qdrant client to avoid file descriptor issues during import
_client = None

def get_qdrant_client():
    """Get or create Qdrant client with lazy initialization"""
    global _client
    if _client is None:
        print(f"Initializing Qdrant client for {QDRANT_HOST}:{QDRANT_PORT}")
        _client = QdrantClient(
            host=QDRANT_HOST, 
            port=QDRANT_PORT,
            timeout=10,  # Shorter timeout to prevent hanging connections
            prefer_grpc=False,  # Use HTTP instead of gRPC to reduce file descriptor usage
            https=False,  # Explicitly disable HTTPS
            # Additional settings to minimize file descriptor usage
        )
        print("Qdrant client initialized successfully")
    return _client

class AnimalQueryHandler:
    def __init__(self, client_func, collection_name):
        self.get_client = client_func  # Store the function to get client
        self.collection_name = collection_name
    
    def parse_query(self, query):
        """Parse natural language query and determine intent"""
        query = query.lower().strip()
        
        # Query patterns and their corresponding handlers
        patterns = [
            (r'wild|untamed|feral', 'wild_animals'),
            (r'tame|domestic|domesticated|pet', 'tame_animals'),
            (r'easiest.*train|most.*trainable|easy.*tame', 'most_trainable'),
            (r'hardest.*train|least.*trainable|hard.*tame', 'least_trainable'),
            (r'most.*endangered|extinction|rare', 'most_endangered'),
            (r'least.*endangered|safe|common', 'least_endangered'),
            (r'all.*animals|list.*all|show.*all', 'all_animals'),
        ]
        
        for pattern, intent in patterns:
            if re.search(pattern, query):
                return intent
        
        return 'general_search'
    
    def get_wild_animals(self):
        """Get animals marked as wild"""
        try:
            client = self.get_client()
            results = client.scroll(
                collection_name=self.collection_name,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="is_wild",
                            match=MatchValue(value="yes")
                        )
                    ]
                ),
                limit=100,
                with_vectors=True  # Explicitly request vectors
            )
            return [{"creature": point.payload["creature"], 
                    "trainability": point.vector[0], 
                    "endangered": point.vector[1]} for point in results[0]]
        except Exception as e:
            print(f"Error getting wild animals: {e}")
            return []
    
    def get_tame_animals(self):
        """Get animals marked as tame/domestic"""
        try:
            client = self.get_client()
            results = client.scroll(
                collection_name=self.collection_name,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="is_wild",
                            match=MatchValue(value="no")
                        )
                    ]
                ),
                limit=100,
                with_vectors=True  # Explicitly request vectors
            )
            return [{"creature": point.payload["creature"], 
                    "trainability": point.vector[0], 
                    "endangered": point.vector[1]} for point in results[0]]
        except Exception as e:
            print(f"Error getting tame animals: {e}")
            return []
    
    def get_all_animals(self):
        """Get all animals"""
        try:
            client = self.get_client()
            results = client.scroll(
                collection_name=self.collection_name,
                with_vectors=True,
                limit=100
            )
            return [{"creature": point.payload["creature"], 
                    "is_wild": point.payload["is_wild"],
                    "trainability": point.vector[0], 
                    "endangered": point.vector[1]} for point in results[0]]
        except Exception as e:
            print(f"Error getting all animals: {e}")
            return []
    
    def get_most_trainable(self):
        """Get animals sorted by trainability (highest first)"""
        animals = self.get_all_animals()
        return sorted(animals, key=lambda x: x["trainability"], reverse=True)
    
    def get_least_trainable(self):
        """Get animals sorted by trainability (lowest first)"""
        animals = self.get_all_animals()
        return sorted(animals, key=lambda x: x["trainability"])
    
    def get_most_endangered(self):
        """Get animals sorted by endangered status (highest first)"""
        animals = self.get_all_animals()
        return sorted(animals, key=lambda x: x["endangered"], reverse=True)
    
    def get_least_endangered(self):
        """Get animals sorted by endangered status (lowest first)"""
        animals = self.get_all_animals()
        return sorted(animals, key=lambda x: x["endangered"])
    
    def process_query(self, query):
        """Process the query and return appropriate response"""
        intent = self.parse_query(query)
        
        if intent == 'wild_animals':
            animals = self.get_wild_animals()
            return {
                "intent": "Wild Animals",
                "animals": animals,
                "message": f"Found {len(animals)} wild animals."
            }
        
        elif intent == 'tame_animals':
            animals = self.get_tame_animals()
            return {
                "intent": "Tame/Domestic Animals",
                "animals": animals,
                "message": f"Found {len(animals)} tame/domestic animals."
            }
        
        elif intent == 'most_trainable':
            animals = self.get_most_trainable()
            return {
                "intent": "Most Trainable Animals",
                "animals": animals[:3],  # Top 3
                "message": f"The most trainable animal is {animals[0]['creature']} with trainability score {animals[0]['trainability']}" if animals else "No animals found."
            }
        
        elif intent == 'least_trainable':
            animals = self.get_least_trainable()
            return {
                "intent": "Least Trainable Animals",
                "animals": animals[:3],  # Bottom 3
                "message": f"The least trainable animal is {animals[0]['creature']} with trainability score {animals[0]['trainability']}" if animals else "No animals found."
            }
        
        elif intent == 'most_endangered':
            animals = self.get_most_endangered()
            return {
                "intent": "Most Endangered Animals",
                "animals": animals[:3],  # Top 3
                "message": f"The most endangered animal is {animals[0]['creature']} with endangerment score {animals[0]['endangered']}" if animals else "No animals found."
            }
        
        elif intent == 'least_endangered':
            animals = self.get_least_endangered()
            return {
                "intent": "Least Endangered Animals",
                "animals": animals[:3],  # Bottom 3
                "message": f"The least endangered animal is {animals[0]['creature']} with endangerment score {animals[0]['endangered']}" if animals else "No animals found."
            }
        
        elif intent == 'all_animals':
            animals = self.get_all_animals()
            return {
                "intent": "All Animals",
                "animals": animals,
                "message": f"Found {len(animals)} animals in the database."
            }
        
        else:
            # General search - return all animals
            animals = self.get_all_animals()
            return {
                "intent": "General Search",
                "animals": animals,
                "message": f"I'm not sure exactly what you're looking for, but here are all {len(animals)} animals in the database. Try asking about 'wild animals', 'easiest to train', or 'most endangered'."
            }

# Initialize query handler
query_handler = AnimalQueryHandler(get_qdrant_client, collection_name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({'error': 'No query provided'}), 400
        
        result = query_handler.process_query(user_query)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Error processing query: {str(e)}'}), 500
    
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Animal Chat App is running'}), 200

@app.route('/dbhealth')
def dbhealth():
    try:
        # Test Qdrant connection using lazy client
        client = get_qdrant_client()
        info = client.get_collection(collection_name)
        return jsonify({'status': 'healthy', 'collection': collection_name})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == "__main__":
    import os
    import resource
    
    # Set additional environment variables to prevent file watching
    os.environ['FLASK_DISABLE_FILE_WATCHERS'] = '1'
    os.environ['FLASK_ENV'] = 'production'
    os.environ['FLASK_DEBUG'] = 'False'
    
    print("Starting Flask server")
    print(f"Connecting to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}")

    # Use basic Flask app.run() for Gunicorn compatibility
if __name__ == "__main__":
    print("I am being hit! ouch")
    app.run(host="0.0.0.0", port=5000)