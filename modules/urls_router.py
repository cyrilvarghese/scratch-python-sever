# urls_router.py
from fastapi import APIRouter,HTTPException
from dotenv import load_dotenv
from modules.url_loader import web_url_to_text 
from typing import List
from modules.file_handler import write_data_to_file,read_data_from_file
from modules.file_processor import process_files
load_url_router = APIRouter()

@load_url_router.post("/")
async def load_urls(req_body: dict):
    urls=req_body.get("urls")
    try:
        # Call your function to process the URLs
        if urls:
            write_data_to_file(urls)    
            if not isinstance(urls, list):
                raise HTTPException(status_code=400, detail='Invalid data format. Please provide an array of URLs and a question string.')
          
        print("Writing text to files  ----")
        if read_data_from_file():
            web_url_to_text(read_data_from_file());
        await process_files();
        print("Web URLs processing complete ----")

        
        return {"message": "URLs processed successfully"}
    except Exception as e:
        return {"error": str(e)}