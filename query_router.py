# query_router.py
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from modules.url_loader import web_url_to_text # Adjust the path accordingly
from modules.get_retriever import get_retriever  # Adjust the path accordingly
from modules.file_handler import read_data_from_file
from modules.unique_docs import extract_unique_documents
from sentence_transformers import CrossEncoder

load_dotenv()
query_router = APIRouter()
router = APIRouter()

@query_router.post('/')
async def process_request(req_body: dict):
    try:
        # urls = req_body.get("urls")
        question = req_body.get("question")
        num_of_results = int(req_body.get("results"))
        if not isinstance(question, str):
            raise HTTPException(status_code=400, detail='Invalid data format. Please provide an array of URLs and a question string.')
            
        # print("Web URLs processing ----")
        # if read_data_from_file():
        #     web_url_to_text(read_data_from_file());
        
        # print("Web URLs processing complete ----")
    
        retriever =get_retriever(num_of_results);
     
        relevant_docs =   retriever.get_relevant_documents(question)
        print("Relevant docs  -----", len(relevant_docs))

        unique_docs, unique_contents = extract_unique_documents(relevant_docs)
        print("unique docs  -----", len(unique_contents))

        cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        pairs = []
        for doc in unique_contents:
            pairs.append([question, doc])
        
        scores = cross_encoder.predict(pairs)
        print(scores)
        scored_docs = zip(scores, unique_contents)
        sorted_docs = sorted(scored_docs, reverse=True)
       
        # Extracting text from each tuple item
        text_only_list = [item[1] for item in sorted_docs]
       
        # text_array = [doc.page_content for doc in sorted_docs]
        return text_only_list

    except Exception as e:
        print('Error processing request:', e)
        raise HTTPException(status_code=500, detail='Internal Server Error.')

# Example usage:
# Create FastAPI instance and include this router
# app.include_router(router, prefix="/api/query")
