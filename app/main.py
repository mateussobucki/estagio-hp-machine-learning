from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import chat

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],
  allow_methods=["*"],
  allow_headers=["*"],
)

class Req(BaseModel):
  session_id: str
  message: str

@app.post("/chat")
def chat_endpoint(req: Req):
  try:
    return {"reply": chat(req.session_id, req.message)}
  except Exception as e:
    print(f"[chat error] {str(e)}")
    return {"reply": "An error occurred while trying to process your question"}