import langchain
print(langchain.__version__)

import os
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("GOOGLE_API_KEY")


from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

model = init_chat_model("google_genai:gemini-2.5-flash")

class Cricket(BaseModel):
    name : str = Field(description="Name of a popular format")
    duration : float = Field(description="Please tell the duration it is played")
    is_international : bool = Field(description="Whether the format is an international format")
    no_of_teams : int = Field(description="Number of teams playing in it")

#model_with_structure = model.with_structured_output(Cricket)

#response1 = model.invoke("Describe the Cricket class")

#response2 = model_with_structure.invoke("Describe the Cricket class")

#print(response1.content)

#print("#" * 50)

#print(response2)

class CricketProfile(BaseModel):
    name : str
    role : str
    country : str

class PlayerInfo(BaseModel):
    format : str
    players : list[CricketProfile]

model_with_Structure = model.with_structured_output(PlayerInfo)

response = model_with_Structure.invoke("Provide me 3 ODI all rounder International players")

print(response)
