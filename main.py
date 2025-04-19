import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import openai
import uvicorn

# Load environment variables from a .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set OpenAI API key from environment variable

# Initialize the FastAPI application
app = FastAPI()

# Mount the "static" directory to serve static files (e.g., CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates for rendering HTML
templates = Jinja2Templates(directory="templates")

# Route to render the form (GET request)
@app.get("/", response_class=HTMLResponse)
async def render_form(request: Request):
    """
    Render the main form page.
    """
    return templates.TemplateResponse("index.html", {"request": request})

# Route to handle chat messages (POST request)
@app.post("/chat", response_class=HTMLResponse)
async def handle_chat(request: Request, message: str = Form(...)):
    """
    Handle user chat input and return a response from OpenAI's GPT model.
    """
    try:
        # Call OpenAI's ChatCompletion API with the user's message
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
            max_tokens=300
        )
        # Extract the reply from the API response
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        # Handle any errors and return an error message
        reply = f"Error: {str(e)}"
    
    # Render the response back to the user
    return templates.TemplateResponse("index.html", {
        "request": request,
        "response": reply
    })

# Entry point for running the application
if __name__ == "__main__":
    # Get the port from environment variables or use default (10000)
    port = int(os.getenv("PORT", 10000))
    # Run the application with Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)