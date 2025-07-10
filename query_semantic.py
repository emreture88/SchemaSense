# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 14:32:37 2025

@author: Emre.Ture
"""

from ollama import Client as OllamaClient
from qdrant_client import QdrantClient
from qdrant_client.models import SearchRequest
import pprint

OLLAMA_MODEL = "nomic-embed-text"
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "mysql_schema"

ollama = OllamaClient(host='http://localhost:11434')
qdrant = QdrantClient(url=QDRANT_URL)

def embed(text: str):
    response = ollama.embeddings(model=OLLAMA_MODEL, prompt=text)
    return response["embedding"]

def semantic_search(query: str, top_k=3):
    query_vector = embed(query)
    
    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )

    return [{
        "score": r.score,
        "table": r.payload.get("table"),
        "description": r.payload.get("description")
    } for r in results]

if __name__ == "__main__":
    print("Doğal dilde sorgu girin (örnek: 'Son 30 gündeki siparişleri ve kullanıcıları getir'):")
    user_query = input("> ")
    matches = semantic_search(user_query)

    print("\n En yakın eşleşen tablolar:\n")
    for match in matches:
        pprint.pprint(match)
------------------------------

generate_sql.py
------------------------------
from ollama import Client as OllamaClient
from query_semantic import semantic_search

OLLAMA_CHAT_MODEL = "llama3"  # Veya 'mistral', 'codellama', vs.
ollama = OllamaClient(host='http://localhost:11434')

def generate_sql(natural_query: str, matched_table_info: dict):
    table_description = matched_table_info['description']
    
    prompt = f"""
Sen bir SQL uzmanısın. Aşağıdaki tablo yapısını kullanarak verilen kullanıcı isteğine uygun SQL sorgusu yaz.

Tablo Tanımı:
{table_description}

Kullanıcı Sorusu:
{natural_query}

Cevap sadece SQL kodu olsun.
"""
    response = ollama.chat(model=OLLAMA_CHAT_MODEL, messages=[
        {"role": "user", "content": prompt}
    ])

    return response['message']['content']

if __name__ == "__main__":
    print("Doğal dilde sorgu girin:")
    user_input = input("> ")

    matches = semantic_search(user_input)
    best_match = matches[0] if matches else None

    if not best_match:
        print("Uygun eşleşme bulunamadı.")
    else:
        print(f"\n Eşleşen tablo: {best_match['table']}")
        print(f" Açıklama: {best_match['description']}\n")
        
        sql_query = generate_sql(user_input, best_match)
        print(" Oluşturulan SQL Sorgusu:\n")
        print(sql_query)