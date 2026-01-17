from ingestion import ingest
from chunking import chunk_threads
from classify import classify_chunks, save_chunks, load_chunks
from vector_storing import index_chunks
import os

classified_data_path = "data/classified_chunks.json"

if os.path.exists(classified_data_path):
    print("Loading classified chunks from disk...")
    classified_chunks = load_chunks(classified_data_path)
else:
    threads = ingest("data/mock_slack.json")
    chunks = chunk_threads(threads)
    classified_chunks = classify_chunks(chunks)
    save_chunks(classified_chunks, classified_data_path)

index_chunks(classified_chunks)