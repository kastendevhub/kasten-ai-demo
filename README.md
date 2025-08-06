# README

## Install Qdrant from helm

helm repo add qdrant https://qdrant.github.io/qdrant-helm
helm install qdrant qdrant -n qdrant --create-namespace

## Port-forward the qdrant pod to your localhost

kubectl port-forward -n qdrant qdrant-0 6333:6333

## Populate the qdrant database with a collection

python3 populate_qdrant.py

## Create the blueprint

kubectl --namespace=kasten-io create -f qdrant_appconsistent.yaml

## Annotate the qdrant statefulset

kubectl annotate statefulset qdrant kanister.kasten.io/blueprint='qdrant-hooks' \
     --namespace=qdrant

## Create and run a backup policy in Kasten for qdrant
