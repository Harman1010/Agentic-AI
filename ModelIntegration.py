import langchain
print(langchain.__version__)

import os
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("GOOGLE_API_KEY")


from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
)

#l = 0
#for chunks in model.stream("Write a summary of Harry Potter in 100 words"):
    #temp = chunks.content
    #l = l + len(temp)
    #print(chunks.content,end=" ",flush = True)

#print(l)

#l = 0
#for chunks in model.stream("Write a summary of Harry Potter in 100 words"):
    #temp = chunks.content
    #l = l + len(temp)
    #print(chunks.content,end="",flush = True)


responses = model.batch([
    "What are some of the best places to visit in Paris?",
    "What are some of the best places to visit in New York?",
    "What are some of the best places to visit in London?",
])
d = []
for response in responses:
    d.append(response.content[:100])

print(d[0])

    
