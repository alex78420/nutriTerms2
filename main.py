from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
from terms import analyze_terms_content, generate_summary
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://YOUR-EXTENSION-ID"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str
    content: str

class SummaryRequest(BaseModel):
    content: str
    model_type: Optional[str] = 'models/gemini-1.5-flash-001'

@app.post("/api/analyze")
async def analyze_terms(request: AnalyzeRequest) -> Dict[str, Any]:
    try:
        # Analyze the content directly
        result = analyze_terms_content(request.content, request.url)
        
        if result['status'] == 'error':
            raise HTTPException(status_code=400, detail=result['message'])
        
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/summarize")
async def summarize_content(request: SummaryRequest) -> Dict[str, Any]:
    try:
        if not request.content:
            raise HTTPException(status_code=400, detail="No content provided")

        summary = generate_summary(request.content, request.model_type)
        
        if isinstance(summary, str) and summary.startswith("Error generating summary:"):
            raise HTTPException(status_code=500, detail=summary)
        
        return {
            "status": "success",
            "data": {
                "summary": summary
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
