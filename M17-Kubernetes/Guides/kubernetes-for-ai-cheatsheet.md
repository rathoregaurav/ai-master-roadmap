# Kubernetes For AI Cheatsheet

## Common AI Workloads

| Workload | Kubernetes object |
| --- | --- |
| FastAPI app | Deployment + Service |
| Background worker | Deployment |
| Scheduled eval job | CronJob |
| Vector database | StatefulSet or managed service |
| Model server | Deployment with GPU node selector |
| Internal tool connector | Deployment + Service |

## Beginner Commands To Learn Later

```bash
kubectl get pods
kubectl get services
kubectl describe pod <name>
kubectl logs <pod>
kubectl apply -f deployment.yaml
kubectl rollout status deployment/ai-api
```

## What To Watch

- pod restarts
- CPU and memory usage
- failed readiness probes
- image pull errors
- service routing problems

