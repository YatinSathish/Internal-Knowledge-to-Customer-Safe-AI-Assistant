import chromadb
from google import genai
import os
from vector_storing import chroma_client, embed_text

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
collection = chroma_client.get_collection(name="knowledge_chunks")

def run_qa(question, is_customer):
    query_vector = embed_text(question)
    # fetching chunks explicitly marked as customer_safe
    where_filter = {"customer_safe": True} if is_customer else None
    
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=5,
        where=where_filter
    )

    context_parts = []
    citations = []
    
    for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
        label = f"SOURCE_{i+1}"
        sot_tag = "[OFFICIAL/AUTHORITATIVE]" if meta['source_of_truth'] else "[DISCUSSION]"
        context_parts.append(f"{label} {sot_tag}: {doc}")
        
        if is_customer:
            citations.append({"id": label, "source": "Official Support Channel"})
        else:
            # Showing all details for internal users
            citations.append({"id": label, "source": f"Slack #{meta['channel']}", "thread": meta['thread_id']})

    prompt = f"""
    You are an AI assistant. Use the context below to answer: {question}
    
    CRITICAL RULES:
    - If a source is marked [OFFICIAL/AUTHORITATIVE], prioritize it over [DISCUSSION].
    - If sources contradict, state the official policy first.
    - Cite sources using [SOURCE_X].
    - If no customer-safe sources exist and is_customer=True, say 'Insufficient public documentation available.'
    
    Context:
    {"\n".join(context_parts)}
    """

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return {"answer": response.text, "citations": citations}