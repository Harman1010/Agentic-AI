import langchain
print(langchain.__version__)

import os
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("GOOGLE_API_KEY")


from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from langchain.agents.middleware import SummarizationMiddleware,HumanInTheLoopMiddleware
from langchain.messages import HumanMessage
from langchain.tools import tool
from langgraph.types import Command
from langgraph.checkpoint.memory import InMemorySaver

model = init_chat_model("google_genai:gemini-2.5-flash")

agent = create_agent(
    model = model,
    middleware = [SummarizationMiddleware(
        model = model,
        trigger = ("messages",10),
        keep = ("messages",1-0)
    )],
)
### Run with thread id
config={"configurable":{"thread_id":"test-1"}}

questions = [
    "What is 2+2?",
    "What is 10*5?",
    "What is 100/4?",
    "What is 15-7?",
    "What is 3*3?",
    "What is 4*4?",
]

#for q in questions:
    #response=agent.invoke({"messages":[HumanMessage(content=q)]},config)
    #print(f"Messages: {response}")
    #print(f"Messages: {len(response['messages'])}")

#Token

@tool
def search_hotels(city : str):
    """Search the hotels and return a long detailed answer"""
    return f"""Hotels in {city}
    1.Luxury hotel : 100000/day 2.Premium hotel : 50000/day 3.Budget hotel : 10000/day"""

agent = create_agent(
    model = model,
    tools = [search_hotels],
    middleware = [SummarizationMiddleware(
        model = model,
        trigger = ("tokens",500),
        keep = ("tokens",100)
    )],
)

config={"configurable":{"thread_id":"test-1"}}

def count_tokens(messages):
    total_chars = sum(len(str(m.content)) for m in messages)
    tokens = total_chars // 4
    return tokens

cities = ["agra","mumbai","london","new york","paris","tokyo","sydney"]

#for city in cities:
    #response = agent.invoke({"messages" : [HumanMessage(content=f"Find hotels in {city}")]},config)
    #token_count = count_tokens(response['messages'])
    #print(f"Tokens: {token_count}")
    #print(f"Content: {response['messages'][-1].content}")


#HITL

def send_email(body : str,recipient : str,subject : str):
    """Sends an email to the recipient"""
    return f"Email sent to {recipient} with subject {subject} and body {body}"

def read_email(email : str):
    """Reads an email"""
    return f"Email read successfully for mail id : {email}"

agent = create_agent(
    model = model,
    tools = [send_email,read_email],
    checkpointer = InMemorySaver(),
    middleware = [HumanInTheLoopMiddleware(
        interrupt_on = {
            "send_email" : 
            {"allowed_decisions" : ["approve","edit","reject"]},
            "read_email" : False
        }
    )]
)
config = {"configurable": {"thread_id": "test-approve"}}
response = agent.invoke({"messages" : [HumanMessage(content = "Send email to john@test.com with subject 'Hello' and body 'How are you?'")]},config=config)
print(response['messages'][-1].content)

if "__interrupt__" in response:
    print("User Interrupted")

    response = agent.invoke(
        Command(resume = {
            "decisions" : [{"type" : "reject"}]
        }),config=config
    )

    print(f"Response : {response['messages'][-1].content}")

