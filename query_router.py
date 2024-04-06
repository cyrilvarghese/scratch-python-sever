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

    
        retriever =get_retriever(num_of_results);
     
        relevant_docs =   retriever.get_relevant_documents(question)
        print("Relevant docs  -----", len(relevant_docs))

        unique_docs, unique_content_details = extract_unique_documents(relevant_docs)
        print("unique docs  -----", len(unique_content_details))

        cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
     
        pairs = []
        for content_detail in unique_content_details:
            # Extract the 'page_content' for scoring
            page_content = content_detail["page_content"]
            pairs.append([question, page_content])

        # Assume cross_encoder.predict() is a method that scores pairs of question and page_content
        scores = cross_encoder.predict(pairs)

        # Immediately after scoring, print scores with URL source for verification
        for score, content_detail in zip(scores, unique_content_details):
            print(f"Score: {score}, URL Source: {content_detail['url_source']}")

        # Combine the scores with the corresponding content details
        scored_content_details = zip(scores, unique_content_details)

        # Sort the combined list based on scores in descending order (higher scores are better)
        sorted_content_details = sorted(scored_content_details, reverse=True, key=lambda x: x[0])

        # Print sorted scores with URL source for verification
        print("\nSorted Scores and URL Sources:")
        for score, content_detail in sorted_content_details:
            print(f"Score: {score}, URL Source: {content_detail['url_source']}")






        # Extracting text from each tuple item
        text_only_list = [item[1] for item in sorted_content_details]
       
        # text_array = [doc.page_content for doc in sorted_docs]
        return text_only_list

    except Exception as e:
        print('Error processing request:', e)
        raise HTTPException(status_code=500, detail='Internal Server Error.')

# Example usage:
# Create FastAPI instance and include this router
# app.include_router(router, prefix="/api/query")
