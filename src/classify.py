import os
from datamodels import Chunk
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

client = genai.Client(api_key=GEMINI_API_KEY)

def classifier(chunk: Chunk):
    prompt = f"""
                You are a system that classifies internal company conversations.

                Definitions:
                - Knowledge worthy: Information useful for answering future questions (decisions, policies, confirmed fixes, official answers). Excludes brainstorming, opinions, complaints, or speculation.
                - Source of truth: A final, authoritative decision, policy, or confirmed resolution that overrides earlier discussion.
                - Customer safe: Information that is safe to share with external customers. Excludes sensitive internal discussions, internal debate, or admissions of technical debt.

                Conversation chunk:
                \"\"\"
                {chunk.text}
                \"\"\"

                Return STRICT JSON with:
                - knowledge_worthy (boolean)
                - source_of_truth (boolean)
                - customer_safe (boolean)
                - reason (short explanation)
            """
    response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=prompt,
    config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )
    raw_text = response.text.strip()

    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError:
        # raise ValueError(f"Invalid JSON from Gemini:\n{raw_text}")
        clean_text = raw_text.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean_text)
    chunk.knowledge_worthy = result["knowledge_worthy"]
    chunk.source_of_truth = result["source_of_truth"]
    chunk.customer_safe = result["customer_safe"]
    chunk.classification_reason = result["reason"]

    return chunk

def classify_chunks(chunks):
    classified = []
    for chunk in chunks:
        classified.append(classifier(chunk))
    return classified