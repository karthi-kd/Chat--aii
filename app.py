from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(
    prompt: str = Form(""),
    image: UploadFile = File(None)
):
    try:
        # If ONLY text
        if image is None:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful AI named Karthi AI."},
                    {"role": "user", "content": prompt}
                ]
            )
            reply = response.choices[0].message.content
            return {"reply": reply}

        # If image is included
        img_bytes = await image.read()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI named Karthi AI."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt if prompt else "Analyze this image"},
                        {"type": "input_image", "image": img_bytes}
                    ]
                }
            ]
        )

        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Server error: {str(e)}"}
        

