import os
import tempfile
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from rag_engine import RAGEngine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="RAG AI Assistant API")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Global RAG engine instance
# Note: For production with multiple workers, you'd need a shared store (like Redis/Pinecone)
# but for a single-container deployment, this in-memory instance works.
rag_engine = RAGEngine()

class ChatRequest(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main chat interface."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handle PDF upload and indexing."""
    if not file.filename.endswith(".pdf"):
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid file type. Please upload a PDF."}
        )
    
    # Create a temporary file
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            shutil.copyfileobj(file.file, tmp_file)
            tmp_path = tmp_file.name
        
        # Process the file
        status = rag_engine.process_pdf(tmp_path)
        
        return {"message": status}
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        # Cleanup
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)

@app.post("/chat")
async def chat(request: ChatRequest):
    """Handle chat queries."""
    if not request.question:
        raise HTTPException(status_code=400, detail="No question provided")
    
    try:
        response, sources = rag_engine.query(request.question)
        
        # Format sources for frontend
        source_list = [
            {"content": doc.page_content, "metadata": doc.metadata} 
            for doc in sources
        ]
        
        return {
            "response": response,
            "sources": source_list
        }
    except ValueError as e:
        # Usually happens if RAG engine isn't initialized with a doc
        return JSONResponse(status_code=400, content={"error": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
