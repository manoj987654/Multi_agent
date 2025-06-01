import os
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import traceback
import json  # Add this for JSON parsing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("email-agent")

app = FastAPI(
    title="Email Processing Agent",
    description="API for processing email files",
    version="1.0.0",
    max_upload_size=10 * 1024 * 1024,  # 10MB limit
)

# Create upload directory if not exists
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)

def process_email_content(content: str) -> dict:
    """Example processing function - customize with your logic"""
    return {
        "word_count": len(content.split()),
        "line_count": len(content.splitlines()),
        "sender": extract_sender(content)
    }

def extract_sender(content: str) -> str:
    for line in content.splitlines():
        if line.lower().startswith("from:"):
            return line[5:].strip()
    return "unknown@domain.com"

@app.post("/process")
async def process_email(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing file: {file.filename}")
        
        # Validate file type
        if not (file.filename.endswith(".txt") or file.filename.endswith(".json")):
            raise HTTPException(400, "Only .txt and .json files are supported")
        
        file_path = UPLOAD_DIR / file.filename

        # Handle .json files
        if file.filename.endswith(".json"):
            try:
                # Read and parse JSON
                data = json.load(file.file)
                # Save JSON file
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                return JSONResponse({
                    "status": "success",
                    "filename": file.filename,
                    "results": data,  # Returning the JSON data directly
                    "saved_path": str(file_path)
                })
            except json.JSONDecodeError:
                logger.error("Invalid JSON file")
                raise HTTPException(400, "Invalid JSON file")
        
        # Handle .txt files
        content = (await file.read()).decode("utf-8")
        result = process_email_content(content)
        
        # Save text file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return JSONResponse({
            "status": "success",
            "filename": file.filename,
            "results": result,
            "saved_path": str(file_path)
        })
    
    except UnicodeDecodeError:
        logger.error("Invalid text encoding")
        raise HTTPException(400, "File must be UTF-8 encoded text")
    
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(500, f"Processing error: {str(e)}")

@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "Email Processing Agent",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
