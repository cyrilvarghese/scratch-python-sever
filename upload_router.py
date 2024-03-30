 # upload_router.py

import os 
from fastapi import APIRouter, File, UploadFile
upload_router = APIRouter()
from modules.crop_pdf_text import save_cropped_text
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import List
import json
from modules.file_processor import process_files

@upload_router.post("/")
async def upload_pdfs(files_data: str = Form(...),pdf_files: list[UploadFile] = File(...)):
    response = {"message": "PDF files uploaded successfully.", "uploaded_files": []}
     # Parse files_data JSON to get cropping info for each file
    try:
        files_info = json.loads(files_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON for file data.")
 
    for pdf_file in pdf_files:

        # Verify each file has its corresponding cropping info
        if not any(pdf_file.filename == info.get("filename") for info in files_info):
            raise HTTPException(status_code=400, detail=f"Missing cropping info for file {pdf_file.filename}.")
   
        # Find this file's cropping info   
        cropping_info = next((info for info in files_info if info["filename"] == pdf_file.filename), None)

        
        if not pdf_file.filename.endswith('.pdf'):
            return {"error": "Only PDF files are allowed."}
        # Specify the directory where files will be saved
        upload_folder = "files"
        os.makedirs(upload_folder, exist_ok=True)  # Create the directory if it doesn't exist
        
        # Save the PDF file to the specified directory
        file_path = os.path.join(upload_folder, pdf_file.filename)
        # Process the PDF file (for example, save it to disk)
        with open(file_path, "wb") as file_object:
            file_object.write(await pdf_file.read())
            
        save_cropped_text(file_path,cropping_info["from_page"], cropping_info["to_page"]);
        # save_cropped_pdf(file_path,33,60);

        response["uploaded_files"].append(pdf_file.filename)
        
    await process_files();
    return response

@upload_router.get("/")
async def get_upload():
    return {"message": "GET Upload route"}
 