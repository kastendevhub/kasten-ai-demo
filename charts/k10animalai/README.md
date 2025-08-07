# Kasten AI Demo Helm Chart

This Helm chart deploys the Kasten AI Demo application with an optional Qdrant vector database.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+

## Installation

### Install with Qdrant (Recommended)

This will deploy both the application and Qdrant database, then populate it with sample data:

```bash
helm install my-k10animalai ./charts/k10animalai
```

### Install without Qdrant

If you have an external Qdrant instance:

```bash
helm install my-k10animalai ./charts/k10animalai \
  --set qdrant.enabled=false \
  --set qdrant.host=your-external-qdrant-host
```

## Configuration

### Key Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `qdrant.enabled` | Enable Qdrant subchart deployment | `true` |
| `qdrant.populateJob.enabled` | Enable the job to populate Qdrant with sample data | `true` |
| `qdrant.host` | Qdrant host (used when external) | `"qdrant"` |
| `qdrant.port` | Qdrant port | `"6333"` |
| `service.type` | Kubernetes service type | `LoadBalancer` |
| `k10animalai.replicaCount` | Number of application replicas | `1` |

### Qdrant Configuration

When `qdrant.enabled` is `true`, the chart will:

1. Deploy a Qdrant instance using the Bitnami Qdrant chart
2. Wait for Qdrant to be ready
3. Run a post-install job to populate the database with sample animal data
4. Start the application

## Components Deployed

When fully deployed with Qdrant enabled, you will have:

1. **Qdrant Pod**: Vector database for storing embeddings
2. **Application Pod**: Web frontend for the AI demo
3. **Populate Job**: One-time job to seed the database (completes and terminates)

## Access

After deployment, the application will be available through the LoadBalancer service. Get the external IP:

```bash
kubectl get svc
```

## Customization

See `values.yaml` for all available configuration options.

## Dependencies

- bitnami/qdrant: ^1.15.1
