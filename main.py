import os
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_form():
    with open("templates/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/chat", response_class=HTMLResponse)
async def chat(message: str = Form(...)):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
        max_tokens=300
    )
    reply = response.choices[0].message.content.strip()
    return HTMLResponse(f"<p><b>You:</b> {message}</p><p><b>Bot:</b> {reply}</p>")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render sets this automatically
    uvicorn.run(app, host="0.0.0.0", port=port)