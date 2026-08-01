#======Modules=====#
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain
from langchain.agents import create_agent
from tavily import TavilyClient
import pytesseract as pyt
import streamlit as st
import os
import time
import numpy as np



#====Model=========#
model = ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash-lite',
    google_api_key = GOOGLE_API_KEY
)

response = model.invoke("Hello Buddy!")
response.content[-1]["text"]


# Search_latest_info using tavily
def search_latest_info(query):
  """This function helps to give
  latest search using tavily
  based on given user query related research or contents"""

  client = TavilyClient(api_key = TAVILY_API_KEY)
  response = client.search(query)
  return response


# Calling function
search_latest_info("String Theory in Quantum Mechanics")


# Tool 2
def generate_image(img_prompt,slide_no = 1):
  """This function helps user to generate
  image using free api, with given
  img_prompt, with slide no"""

  url = f"https://image.pollinations.ai/{img_prompt}"

  import requests as r
  content = r.get(url).content
  with open(f"ai_image_{slide_no}.jpeg",'wb') as f:
    f.write(content)

  from PIL import Image
  img = Image.open(f"ai_image_{slide_no}.jpeg")
  return img


# Calling function
generate_image("sitting at bornfire with alaskan northen lights in night from person pov")


# leader_agent creation
leader_agent = create_agent(
    model = model,
    tools = [search_latest_info,
             #generate_image
             ])
leader_agent


# Running Agent
def run_agent(leader_agent, query):
  prompt = """Based on Below given Query,
  your task is to call specific tool, first to
  promptify user prompt, than call image tool, or
  latest search if required.give slide dynamic, ui ux,
  with creative design, keep help of function to generate image
  based on given topic,
  Generate image using
  with number of slide asked, and use time sleep to hit image request on server
  and using file handling embed this in output html, use java script function
  give Final response output in HTML, no markdowns
  user query given below:"""

  prompt = prompt+query

  # prompt = agent_prompt(prompt)

  response = leader_agent.invoke({'messages':[{'role':'user',
                                              'content':prompt}]})
  code = response['messages'][-1].content[-1]['text']
  return code


# Creating ppt
user = """Create ppt for Presenter Samir Khan,
Topic: Top 5 wizards in Harry potter series,
Slides: 5 slides"""
code= run_agent(leader_agent, user)
ip.display.HTML(code)

# file saving
with open("ppt.html","w") as f:
  f.write(code)

# Only for colab user to download file
from google.colab import files
files.download("ppt.html")