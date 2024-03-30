import requests
from pydantic import BaseModel, Field
import datetime
import os
import openai
from langchain.agents import tool
from dotenv import load_dotenv, find_dotenv
from langchain.agents import tool
from langchain.tools.render import format_tool_to_openai_function
from langchain.chat_models import ChatOpenAI
load_dotenv()

# Define the input schema
class SlideSchemaInputs(BaseModel):
    layout_type: str = Field(..., description="type of the layout used to render the social media post")
    num_of_slides: int = Field(..., description="number of slide in the social media post")
 
 
@tool(args_schema=SlideSchemaInputs)
def generate_slides(layout_type: str, num_of_slides: int) -> dict:
    """generate the specified number slides for the given layout type"""
     
   
    return f'The layout type is branding and the count id 3'


openAIFunction = format_tool_to_openai_function(generate_slides)


model = ChatOpenAI(temperature=0).bind(functions=openAIFunction)