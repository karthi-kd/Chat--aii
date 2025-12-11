from fastapi import FastAPI, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI(title="My ChatGPT AI")

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
        messages = [
            {"role": "system", "content": "You are a helpful AI named Karthi AI."}
        ]

        # If ONLY text
        if image is None:
            messages.append({"role": "user", "content": prompt})
        else:
            # Read image bytes
            img_bytes = await image.read()
            b64_image = base64.b64encode(img_bytes).decode()

            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt if prompt else "Analyze this image"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{image.content_type};base64,{b64_image}"
                        }
                    }
                ]
            })

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Server error: {str(e)}"}
