import os
import chromadb
import numpy as np
from typing import List
from google import genai
from datamodels import Chunk
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

def embed_text(text: str) -> List[float]:
    response = client.models.embed_content(
        model="models/text-embedding-004",
        contents=text,
    )
    return response.embeddings[0].values


def index_chunks(chunks: List[Chunk]):
    collection = chroma_client.get_or_create_collection(name="knowledge_chunks")
    for chunk in chunks:
        if not chunk.knowledge_worthy:
            continue  

        embedding = embed_text(chunk.text)

        collection.upsert(
            ids=[chunk.chunk_id],
            documents=[chunk.text],
            embeddings=[embedding],
            metadatas=[{
                "channel": chunk.channel,
                "thread_id": chunk.thread_id,
                "source_of_truth": bool(chunk.source_of_truth),
                "customer_safe": bool(chunk.customer_safe),
                "source": "slack",
            }]
        )
    print(f"Indexed {len(collection.get()['ids'])} chunks.")
