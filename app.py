import os
import base64
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables")

client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize FastAPI
app = FastAPI(title="OpenAI Vision Backend")

# CORS middleware (allow all for development; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Root ----------
@app.get("/")
def root():
    return {"status": "OpenAI backend running"}

# ---------- Text Chat Endpoint ----------
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=req.message
        )
        return {"reply": response.output_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------- Image + Text Analysis Endpoint ----------
@app.post("/analyze")
async def analyze(
    image: UploadFile = File(...),
    text: str = Form(...)
):
    try:
        # Read image and convert to base64
        image_bytes = await image.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # Send image + text to OpenAI
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": text},
                    {"type": "input_image", "image_base64": image_base64}
                ]
            }]
        )
        return {"result": response.output_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        





