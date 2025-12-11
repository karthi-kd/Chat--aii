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
        # CASE 1 — TEXT ONLY
        if image is None:
            response = client.responses.create(
                model="gpt-4o-mini",
                input=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt}
                        ]
                    }
                ]
            )
            return {"reply": response.output_text}

        # CASE 2 — TEXT + IMAGE
        # ❗ Do NOT read bytes, send file object
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt if prompt else "Analyze this image"
                        },
                        {
                            "type": "input_image",
                            "image": image.file    # ← CORRECT
                        }
                    ]
                }
            ]
        )

        return {"reply": response.output_text}

    except Exception as e:
        return {"reply": f"Server error: {str(e)}"}
        


