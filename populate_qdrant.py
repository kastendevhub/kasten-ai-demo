
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct
import numpy as np

# Connect to the Qdrant database
client = QdrantClient(host="localhost", port=6333)

# Define the collection name
collection_name = "animal_collection"

# Create the collection with vectors stored on disk
client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=2, distance=Distance.COSINE, on_disk=True)
)

# Fictional animal data with 4-dimensional vectors
animal_data = [
    {"id": 1, "creature": "Dog", "is_wild" : "no", "vector": [0.9, 0.1]},
    {"id": 2, "creature": "Elephant", "is_wild" : "yes", "vector": [0.7, 0.8]},
    {"id": 3, "creature": "Eagle", "is_wild" : "yes", "vector": [0.7, 0.3]},
    {"id": 4, "creature": "Shark", "is_wild" : "yes", "vector": [0.1, 0.6]},
    {"id": 5, "creature": "Kangaroo", "is_wild" : "yes", "vector": [0.3, 0.1]},
    {"id": 6, "creature": "Cat", "is_wild" : "no", "vector": [0.3, 0.1]},
    {"id": 7, "creature": "Pachyderm", "is_wild" : "yes", "vector": [0.4, 0.8]},
    {"id": 8, "creature": "Mastadon", "is_wild" : "yes", "vector": [0.2, 0.9]},
]

# Convert animal data to Qdrant PointStruct format
points = [
    PointStruct(id=animal["id"], vector=np.array(animal["vector"]), payload={"creature": animal["creature"], "is_wild": animal["is_wild"]})
    for animal in animal_data
]

# Upload the points to the collection
client.upsert(collection_name=collection_name, points=points)

print(f"Successfully populated the '{collection_name}' collection with fictional animal data.")
