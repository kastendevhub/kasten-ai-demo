# README

Install Qdrant from helm, then portforward the pod to your local host on port 6333

Populate the qdrant database with a collection

python3 populate_qdrant.py

Create the blueprint

kubectl --namespace=kasten-io create -f qdrant_appconsistent.yaml

Annotate the qdrant statefulset

kubectl annotate statefulset qdrant kanister.kasten.io/blueprint='qdrant-hooks' \
     --namespace=qdrant

