from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
##This class is to manage chat session history. We can delete the session and the history
## based on inactive time elapsed. Functionality is not coded yet but that can be an extension
class SessionManager:
  store = {}
  def get_session_history(self, session_id: str):
    if session_id not in self.store:
      self.store[session_id] = ChatMessageHistory()
    return self.store[session_id]
  
