import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
async def generate(request: Request):
    try:
        body = await request.json()
        prompt = body.get("prompt")

        if not prompt:
            return JSONResponse(
                {"error": "Prompt is required"},
                status_code=400
            )

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": "Generate only valid HTML code. No explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return JSONResponse({
            "html": response.output_text
        })

    except Exception as e:
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )









