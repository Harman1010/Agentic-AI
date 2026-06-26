import langchain
print(langchain.__version__)

import os
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("GOOGLE_API_KEY")

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage,SystemMessage,HumanMessage,ToolMessage

model = init_chat_model("google_genai:gemini-2.5-flash")

response = model.invoke("What is 2 + 2")

print(response.content)

message = SystemMessage("You are a helpful assistant")

response = model.invoke([message,"What is AI?"])

print(response.content)