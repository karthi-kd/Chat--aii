import os
import base64
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

Load environment variables

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = None
if OPENAI_API_KEY:
client = OpenAI(api_key=OPENAI_API_KEY)
else:
print("⚠️ OPENAI_API_KEY not found")

app = FastAPI(title="OpenAI Vision Backend")

CORS

app.add_middleware(
CORSMiddleware,
allow_origins=[""],
allow_methods=[""],
allow_headers=["*"],
)

---------------- ROOT ----------------

@app.get("/")
def root():
return {"status": "OpenAI backend running"}

---------------- TEXT CHAT ----------------

class ChatRequest(BaseModel):
message: str

@app.post("/chat")
async def chat(req: ChatRequest):
if not client:
return {"error": "OpenAI API key not configured"}

try:  
    response = client.responses.create(  
        model="gpt-4.1-mini",  
        input=req.message  
    )  
    return {"reply": response.output_text}  

except Exception as e:  
    return {"error": str(e)}

---------------- IMAGE + TEXT ANALYSIS ----------------

@app.post("/analyze")
async def analyze(
image: UploadFile = File(...),
text: str = Form(...)
):
if not client:
return {"error": "OpenAI API key not configured"}

try:  
    image_bytes = await image.read()  
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")  

    response = client.responses.create(  
        model="gpt-4.1-mini",  
        input=[  
            {  
                "role": "user",  
                "content": [  
                    {  
                        "type": "input_text",  
                        "text": text  
                    },  
                    {  
                        "type": "input_image",  
                        "image_url": f"data:{image.content_type};base64,{image_base64}"  
                    }  
                ]  
            }  
        ]  
    )  

    return {"result": response.output_text}  

except Exception as e:  
    return {"error": str(e)}












