# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 14:31:46 2025

@author: Emre.Ture
"""

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance, CollectionStatus
from ollama import Client as OllamaClient
import hashlib
import json

OLLAMA_MODEL = "nomic-embed-text"  # Ollama'da bu model yüklü olmalı: `ollama pull nomic-embed-text`
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "mysql_schema"

ollama = OllamaClient(host='http://localhost:11434')
qdrant = QdrantClient(url=QDRANT_URL)

def create_collection_if_needed():
    collections = qdrant.get_collections().collections
    if COLLECTION_NAME not in [c.name for c in collections]:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=768,  # nomic-embed-text çıktı boyutu
                distance=Distance.COSINE
            )
        )

def embed(text: str):
    response = ollama.embeddings(model=OLLAMA_MODEL, prompt=text)
    return response["embedding"]

def index_schema(schema):
    points = []
    for table in schema:
        table_name = table["table"]
        description = f"Table `{table_name}` with columns: {', '.join(table['columns'])}."
        if table["foreign_keys"]:
            fks = "; ".join([f"{fk['column']} → {fk['references']}" for fk in table["foreign_keys"]])
            description += f" Foreign keys: {fks}."
        
        vec = embed(description)
        uid = int(hashlib.sha256(description.encode()).hexdigest(), 16) % (10**10)
        points.append(PointStruct(id=uid, vector=vec, payload={
            "table": table_name,
            "description": description
        }))
    
    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)

def load_schema(path="schema.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    create_collection_if_needed()
    schema = load_schema()
    index_schema(schema)
    print("Şema başarıyla Qdrant'a aktarıldı.")