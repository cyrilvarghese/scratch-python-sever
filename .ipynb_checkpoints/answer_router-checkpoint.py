# answer_router.py
from fastapi import APIRouter, Request
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import json
answer_router = APIRouter()

multiple_input_prompt = PromptTemplate(
    input_variables=["topic", "context"],
    template=(
        "You are a seasoned UX expert who explains complex concepts. "
        "Create a linked in post with 5 slide or more given the topic and context. "
        "Use the provided articles delimited by triple quotes to answer questions. "
        'If the answer cannot be found in the articles, write "I could not find an answer". '
        "Return each slide as a json array of <title></title><subtitle></subtitle><body></body>\n"
        '""""""""""topic\n'
        '{topic}\n'
        '"""""""""""""""""\n'
        '"""""""""context-\n'
        '{context}\n'
        '"""""""""""""\n'
    ),
)


class RequestBody(BaseModel):
    topic: str
    texts: str
    creativity: int

@answer_router.post("/")
async def answer(request_data: dict):
    creativity = request_data.get("creativity")
    topic = request_data.get("topic")
    texts = request_data.get("text")
    chat_model = ChatOpenAI(temperature=creativity)
    chain = multiple_input_prompt.pipe(chat_model)
    result = await chain.invoke(
        topic=topic,
        context=texts,
    )
    return json.loads(result.content)
