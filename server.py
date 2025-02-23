from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bot is running!"}

port = int(os.getenv("PORT", 8080))

def run_server():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
