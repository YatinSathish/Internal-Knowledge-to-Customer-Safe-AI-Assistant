from ingestion import ingest
from chunking import chunk_threads
from classify import classify_chunks, save_chunks, load_chunks
from vector_storing import index_chunks
from retrieve import run_qa
import os
import argparse
from api import start_api

classified_data_path = "data/classified_chunks.json"

def run_pipeline():
    if os.path.exists(classified_data_path):
        print("Loading classified chunks from disk...")
        classified_chunks = load_chunks(classified_data_path)
    else:
        threads = ingest("data/mock_slack.json")
        chunks = chunk_threads(threads)
        classified_chunks = classify_chunks(chunks)
        save_chunks(classified_chunks, classified_data_path)

    index_chunks(classified_chunks)
    return classified_chunks

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Central Control: Internal Knowledge Assistant")
    parser.add_argument("--setup", action="store_true", help="Ingest, Classify, and Index data")
    parser.add_argument("--api", action="store_true", help="Launch the FastAPI server")
    parser.add_argument("--query", type=str, help="Run a direct CLI query")
    parser.add_argument("--customer", action="store_true", help="Toggle customer mode for CLI query")

    args = parser.parse_args()

    if args.setup:
        run_pipeline()

    elif args.api:
        # Ensure index exists before starting API
        run_pipeline()
        print("\nLaunching API at http://127.0.0.1:8000/docs")
        start_api()


    elif args.query:
        # Making sure that the DB is loaded
        run_pipeline()
        print(f"\n--- CLI RESULT ({'Customer' if args.customer else 'Internal'}) ---")
        res = run_qa(args.query, is_customer=args.customer)
        print(f"Answer: {res['answer']}")
        print(f"Citations: {res['citations']}")
    else:
        classified = run_pipeline()
        print("\nRunning Default Demo Query")
        q = "What is the API rate limit for v2?"
        internal = run_qa(q, is_customer=False)
        customer = run_qa(q, is_customer=True)
        print(f"Internal Answer: {internal['answer']}")
        print(f"Customer Answer: {customer['answer']}")