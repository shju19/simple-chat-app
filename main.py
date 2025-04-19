import os
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import openai
from fastapi.templating import Jinja2Templates


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    with open("templates/index.html", "r") as f:
        return templates.TemplateResponse("index.html", {"request": request})
        # return HTMLResponse(content=f.read())

@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
        max_tokens=300
    )
    reply = response.choices[0].message.content.strip()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": reply
    })
    # return HTMLResponse(f"<p><b>You:</b> {message}</p><p><b>Bot:</b> {reply}</p>")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render sets this automatically
    uvicorn.run(app, host="0.0.0.0", port=port)