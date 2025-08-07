# Animal Knowledge Chat Application

A natural language chat web application that queries a Qdrant vector database to answer questions about animals and their characteristics.

## Features

- 🐾 Natural language querying (e.g., "Which animals are wild?", "Which is easiest to train?")
- 📊 Interactive web interface with visual animal data
- 🎯 Vector-based similarity search using Qdrant
- 🔄 Real-time query processing
- 📱 Responsive design
- 🚀 Kubernetes-ready with Docker containerization

## Quick Start

Deploy the complete application (including Qdrant vector database) to your Kubernetes cluster using Helm:

### Prerequisites
- Kubernetes cluster (1.19+)
- Helm 3.0+
- kubectl configured for your cluster

### Installation

```bash
# Add the helm repo locally
helm repo add kasten-ai-demo https://veeamkasten.dev/helm/kasten-ai-demo/

# Install with default options
helm install my-demo kasten-ai-demo/k10animalai -n animalai \
--create-namespace
```

### Kasten configuration
A blueprint is available in k8s/ named k10-bp-qdrant.yaml.  Simply create the blueprint with this file
in the `kasten-io` namespace:

```bash
kubectl create -f k8s/k10-bp-qdrant.yaml
kubectl --namespace animalai annotate statefulset/my-demo-qdrant \
    kanister.kasten.io/blueprint=qdrant-hooks
```

This will deploy:
- 🗄️ Qdrant vector database (persistent storage)
- 🤖 Animal chat web application
- 📊 Automatic database population with sample animal data

### Access the Application

```bash
# Get the external IP (for LoadBalancer service)
kubectl get svc -n animalai

# Or port-forward for local access
kubectl port-forward -n animalai svc/my-animal-chat-k10animalai 8080:80
```

Visit `http://localhost:8080` (port-forward) or the external LoadBalancer IP to use the chat interface.

### Cleanup

```bash
helm uninstall animal-chat
```



## Slow Start

### 1. Install Qdrant from helm

```bash
helm repo add qdrant https://qdrant.github.io/qdrant-helm
helm install qdrant qdrant -n qdrant --create-namespace
```

### 2. Port-forward the qdrant pod to your localhost

```bash
kubectl port-forward -n qdrant qdrant-0 6333:6333
```

### 3. Populate the qdrant database with a collection

```bash
python3 populate_qdrant.py
```

### 4. Run the Chat Application Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit `http://localhost:5000` to use the chat interface.

### 5. Deploy to Kubernetes

```bash
# Build and deploy everything
./build-and-deploy.sh
```

Or manually:

```bash
# Build Docker image
docker build -t animal-chat-app:latest .

# Deploy to Kubernetes
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml

# Access via port-forward
kubectl port-forward -n qdrant svc/animal-chat-service 8080:80
```

## Application Architecture

### Data Model
The animal data is stored in Qdrant as 2D vectors where:
- **X-axis (index 0)**: Trainability score (0.0-1.0, higher = more trainable)
- **Y-axis (index 1)**: Endangered status (0.0-1.0, higher = more endangered)

Each animal has metadata including:
- `creature`: Animal name
- `is_wild`: "yes" or "no" indicating wild vs domestic status

### Natural Language Processing
The application recognizes various query patterns:
- **Wild animals**: "wild", "untamed", "feral"
- **Tame animals**: "tame", "domestic", "pet"
- **Trainability**: "easiest to train", "most trainable"
- **Endangered status**: "most endangered", "extinction", "rare"

### Example Queries
- "Which animals are wild?"
- "Which animal is the easiest to train?"
- "Which animals are most endangered?"
- "Show me all animals"
- "Which animals are tame?"

## Kasten Backup Integration

### Create the blueprint

```bash
kubectl --namespace=kasten-io create -f kasten/qdrant_appconsistent.yaml
```

### Annotate the qdrant statefulset

```bash
kubectl annotate statefulset qdrant kanister.kasten.io/blueprint='qdrant-hooks' \
     --namespace=qdrant
```

### Create and run a backup policy in Kasten for qdrant

Use the Kasten dashboard to create a backup policy for the qdrant namespace.
