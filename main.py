from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import uvicorn

# FastAPI App Initialize
app = FastAPI(title="Sovereign AI Workbench Backend")

# CORS Enablement (Browser se API block hone se rokne ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Data Structure
class ChatRequest(BaseModel):
    prompt: str

# Health Check Endpoint
@app.get("/")
def home():
    return {"status": "Sovereign AI Backend Running"}

# Chat Endpoint
@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        # Local Ollama Engine URL
        ollama_url = "http://127.0.0.1:11434/api/generate"
        
        payload = {
            "model": "llama3.2",
            "prompt": request.prompt,
            "stream": False
        }

        # Ollama API call
        response = requests.post(ollama_url, json=payload, timeout=120)

        if response.status_code == 200:
            data = response.json()
            return {"response": data.get("response", "No response generated.")}
        else:
            raise HTTPException(
                status_code=response.status_code, 
                detail="Ollama internal error."
            )

    except requests.exceptions.ConnectionError:
        return {
            "response": "⚠️ Cannot connect to Ollama. Terminal me 'ollama run llama3.2' chalayein."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Direct Python Execution
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)