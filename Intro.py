import langchain
print(langchain.__version__)

import os
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("GOOGLE_API_KEY")


from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

d = {}

def add_new_employee(name:str,pay:int):
    """Add a new employee to the database"""
    d[name] = pay

def get_employee(name:str):
    """Get the pay of employee"""
    if name in d:
        return f"{name}'s pay is {d[name]}"
    else:
        return "Employee not found"

model = init_chat_model("google_genai:gemini-2.5-flash")
agent = create_agent(
    model = model,
    tools = [add_new_employee],
    system_prompt = "You are a helpful assistant"
)

response = agent.invoke({
    "messages" : [{"role" : "user","content":"Add Harman Singh's pay to 1."}]
})

print(response["messages"][-1].content)

agent = create_agent(
    model = model,
    tools = [get_employee],
    system_prompt = "You are a helpful assistant"
)

response = agent.invoke({
    "messages" : [{"role" : "user","content":"Get Harman Singh's pay"}]
})

print(response["messages"][-1].content)