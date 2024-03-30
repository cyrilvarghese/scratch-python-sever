# answer_router.py
import array
from fastapi import APIRouter, Request
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import json
from operator import itemgetter
from modules.websocket_connections  import active_websockets
import json
from langchain_core.output_parsers import StrOutputParser
from modules.template_loader import get_template_by_type
answer_router = APIRouter()


 

# multiple_input_prompt = PromptTemplate(
#     input_variables=["topic", "context"],
#     template=(
#         "You are a seasoned storyteller who understand the 3 part act of story telling."
#         "Create a professional sounding sophiticated presentation given the topic and context.\n The presentation should have good engagement on LinkedIn and a minimum of :  \n - 3 slides \n- catchy titles "
#         "Use the provided context delimited by triple quotes to answer questions.\n "
#         "If the answer cannot be found in the context supplied , write I could not find an answer\n"
#         "Return each slide as a json array of <title></title><subtitle></subtitle><body></body>\n\n\n"
#         '"""topic\n\n\n"'
#         '{topic}\n\n\n"'
#         '"""\n\n\n"'
#         '"""context-\n\n\n"'
#         '{context}\n\n\n"'
#         '"""'
#     ),
# )



multiple_input_prompt = PromptTemplate(
    input_variables=["topic", "context"],
    template=("""
                "You are a seasoned storyteller who understand the 3 part act of story telling."
                "Create a professional sounding sophiticated presentation given the topic and context.\n The presentation should have good engagement on LinkedIn and a minimum of :  \n - 3 slides \n- catchy titles "
                "If the answer cannot be found in the context supplied , write I could not find an answer\n"
                "Generate a JSON-formatted list of slides with a professional tone.The presentation should have good engagement on LinkedIn and a minimum of :  \n - 3 slides and catchy titles ". Ensure each silde is represented as an object within an array. The JSON structure should be as follows:"
                [
                    {{
                        '
                        'Title': '[Slide Title]',
                        'Subtitle': '[Slides Subtitle]',
                        'Body': '[Main content and text body of the slide]',
                        
                    }},
                    {{
                        'Title': '[Slide Title]',
                        'Subtitle': '[Slides Subtitle]',
                        'Body': '[Main content and text body of the slide]',
                    }},
                    {{
                        'Title': '[Slide Title]',
                        'Subtitle': '[Slides Subtitle]',
                        'Body': '[Main content and text body of the slide]',
                    }}
                ]

                "Please adhere to this JSON structure in your response.\n \n context below \n{context}\n \n Topic below \n {topic}"
                """

                )
)

compress_context = PromptTemplate(
    input_variables=["topic", "context"],
    template=(
        "You are an AI assistant compress the given context/topic compress the context into a compelling narrative of bulleted points which can be used to create posts on linked in social media platform "
        '"""topic\n'
        '{topic}\n'
        '"""\n'
        '"""context-\n'
        '{context}\n'
        '"""\n'
    ),
)


# multiple_input_prompt_slides = PromptTemplate(
#     input_variables=["topic", "context"],
#     template=("""
#                 "You are a seasoned storyteller who understand the 3 part act of story telling."
#                 "Create a professional sounding sophisticated slides with a given the topic and context.\n The presentation should have good engagement on LinkedIn and a minimum of :  \n - 3 slides \n "
#                 "If the answer cannot be found in the context supplied , write I could not find an answer\n"
#                 "Generate a JSON-formatted list of slides with a professional tone.The presentation should have good engagement on LinkedIn and a minimum of :  \n - 3 slides and catchy titles ". \n - Ensure each silde is represented as an object within an array \n - the  value key "layout type" is always "branding"\n -The subtitle should be 100 words atleast \n. The JSON structure should be as follows:"
#                 [
#                     {{
#                         "meta": {{
#                                     "layoutType": "branding"
#                                 }},
#                         'title': '[Slide Title]',
#                         'subtitle': '[Slides Subtitle]',
                         
                        
#                     }},
                    
#                     {{
#                         "meta": {{
#                                     "layoutType": "branding"
#                                 }},
#                         'title': '[Slide Title]',
#                         'subtitle': '[Slides Subtitle]',
                         
                        
#                     }},
                    
#                     {{
#                         "meta": {{
#                                     "layoutType": "branding"
#                                 }},
#                         'title': '[Slide Title]',
#                         'subtitle': '[Slides Subtitle]',
                         
                        
#                     }},
#                 ]

#                 "Please adhere to this JSON structure in your response.\n \n context below \n{context}\n \n Topic below \n {topic}"
#                 """

#                 )
# )



@answer_router.post("/")
async def answer(request_data: dict):
    creativity = request_data.get("creativity")
    topic = request_data.get("topic")
    texts = request_data.get("texts")
    layoutType = request_data.get("type")
    # requested_template =get_template_by_topic(topic)  
    requested_template = get_template_by_type(layoutType);

    multiple_input_prompt_slides = PromptTemplate(
        input_variables=["topic", "context"],
        template=requested_template
    )
    chat_model = ChatOpenAI(temperature=creativity)
    chain1 = compress_context | chat_model | StrOutputParser()
    chain2 =(
            { "context" : chain1,"topic":itemgetter("topic")}
            | multiple_input_prompt 
            | chat_model 
            | StrOutputParser()
        )
    chain3 =(
            multiple_input_prompt_slides 
            | chat_model 
            | StrOutputParser()
        )


    result = chain3.invoke({"topic": topic, "context":texts})

    json_str = json.dumps(result)
    
    # Send the JSON string to all active WebSocket connections
    for websocket in active_websockets:
        await websocket.send_text(json_str)
    return result
