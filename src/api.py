from fastapi import FastAPI, HTTPException
from retrieve import run_qa
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="Knowledge Assistant API")

class QueryRequest(BaseModel):
    question: str
    mode: str  # internal or customer

@app.post("/ask")
async def ask_assistant(req: QueryRequest):
    is_customer = (req.mode == "customer")
    try:
        result = run_qa(question=req.question, is_customer=is_customer)

        if is_customer and not result.get("citations"):
            return {
                "answer": "I'm sorry, I have insufficient customer-citable sources to answer this.",
                "citations": [],
                "mode": req.mode
            }
            
        return {
            "answer": result['answer'],
            "citations": result['citations'],
            "mode": req.mode
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def start_api():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


