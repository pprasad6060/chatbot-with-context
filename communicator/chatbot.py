import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from .session_retriever import SessionManager
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
class Chatbot:
  
  def __init__(self):
      # Load environment variables from a .env file
      load_dotenv()
      self.groq_api_key = os.getenv("GROQ_API_KEY")
      self.groq_model = os.getenv("GROQ_MODEL")
      if not self.groq_api_key or not self.groq_model:
          raise ValueError("GROQ_API_KEY and GROQ_MODEL must be set in environment variables.")

      self.model = ChatGroq(model=self.groq_model, api_key=self.groq_api_key)

  def chat_message(self, user_input: str, session_id: str):
    sessionManager = SessionManager()
    #print(f"session History: {sessionManager.get_session_history(session_id)}")
    prompt = self.create_chat_prompt_template()
    chain = prompt | self.model
    print(f"Chain is of type: {type(chain)}")#langchain_core.runnables.base.RunnableSequence
    with_message_history = RunnableWithMessageHistory(
        chain,
        sessionManager.get_session_history,
        input_messages_key="messages"
    )
    response = with_message_history.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config={"configurable": {"session_id": session_id}}
    )
    return response

  def create_chat_prompt_template(self):
    system_message = '''You are a helpful assitant. Answer all the questions 
    to best of you ability with the help of the conversation history provided.'''
    prompt = ChatPromptTemplate.from_messages(
                [("system", system_message),
                  MessagesPlaceholder(variable_name="messages"),
                ]
              )
    return prompt

#   def print_model(self):
#     print(f"Groq Model: {self.model}")
  
# chatbot = Chatbot()
# chatbot.print_model()

  
