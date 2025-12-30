from uuid import uuid4

def create_session_id() -> str:
  random_session_id = uuid4()
  return random_session_id.hex