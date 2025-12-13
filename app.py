import base64
import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="OpenAI Vision Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "OpenAI backend running"}

# ---------- TEXT ONLY CHAT ----------
@app.post("/chat")
async def chat(message: str = Form(...)):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=message
    )
    return {"reply": response.output_text}

# ---------- IMAGE + TEXT ANALYSIS ----------
@app.post("/analyze")
async def analyze(
    image: UploadFile = File(...),
    text: str = Form(...)
):
    image_bytes = await image.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": text},
                {
                    "type": "input_image",
                    "image_base64": image_base64
                }
            ]
        }]
    )

    return {
        "result": response.output_text
    }
        




