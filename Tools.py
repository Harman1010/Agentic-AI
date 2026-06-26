import langchain
print(langchain.__version__)

import os
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("GOOGLE_API_KEY")


from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool

db = {}

@tool
def add_new_employee(name:str,pay:str):
    """Add a new employee to the database"""
    db[name] = pay
    return f"Employee {name} added to the database successfully"

@tool
def get_employee_pay(name:str):
    """Get the pay of an employee"""
    if name in db:
        return f"{name}'s pay is {db[name]}"
    else:
        return "Employee not found"

model = init_chat_model("google_genai:gemini-2.5-flash")

model_with_tools = model.bind_tools([add_new_employee])

response = model_with_tools.invoke("Add a new employee Harman Singh with a pay of 5000")

