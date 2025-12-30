import sys
from pathlib import Path

# Add parent directory to path to import communicator module
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from session_manager.session_creator import create_session_id 
from communicator.chatbot import Chatbot
app = FastAPI()

class chatRequest(BaseModel):
    message: str
    session_id: str | None = None

@app.put("/chat")
async def chat_endpoint(request: chatRequest):
  if request.session_id is None:
      print("No session_id provided, creating a new one.")
      request.session_id = create_session_id()
      print(f"Generated session_id: {request.session_id}")
  chatbot = Chatbot()
  response = chatbot.chat_message(user_input=request.message, session_id=request.session_id)
  return {"response": response, "session_id": request.session_id}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

