from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
import os
import shutil
from app.core.config import settings
from app.core.ai_provider import ai_provider

app = FastAPI(title=settings.APP_NAME)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple In-Memory History for now
chat_history = {}

class ChatRequest(BaseModel):
    message: str
    sessionId: str
    attachments: Optional[List[str]] = []

class ChatResponse(BaseModel):
    id: str
    role: str
    content: str
    timestamp: str
    attachments: Optional[List[str]] = []

# Ensure uploads directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Manage history
    if request.sessionId not in chat_history:
        chat_history[request.sessionId] = []

    history = chat_history[request.sessionId]

    # Handle image attachments if any
    prompt = request.message
    if request.attachments:
        for img_path in request.attachments:
            # Use vision analysis for each image
            analysis = await ai_provider.analyze_image(img_path, "Describe this image briefly.")
            prompt += f"\n[Image Analysis: {analysis}]"

    # Generate response
    response_text = await ai_provider.generate_text(prompt, history)

    # Store in history
    user_msg = {"role": "user", "content": request.message}
    ai_msg = {"role": "assistant", "content": response_text}
    history.append(user_msg)
    history.append(ai_msg)

    return ChatResponse(
        id=str(uuid.uuid4()),
        role="assistant",
        content=response_text,
        timestamp="now", # Simplified
        attachments=request.attachments
    )

@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"url": file_path}

@app.get("/api/history/{session_id}")
async def get_history(session_id: str):
    return chat_history.get(session_id, [])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
