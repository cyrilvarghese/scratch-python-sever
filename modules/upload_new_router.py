 # upload_router.py

import os 
from fastapi import APIRouter, File, UploadFile
from modules.crop_pdf_text import save_cropped_text
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import List
import json
from modules.file_processor import process_files
import fitz  # PyMuPDF
upload_new_router = APIRouter()
files_folder  = "files"
@upload_new_router.post("/")
async def upload_pdfs(pdf_files: list[UploadFile] = File(...)):
    response = {"message": "PDF files uploaded successfully.", "uploaded_files": []}
    for pdf_file in pdf_files:

        if not pdf_file.filename.endswith('.pdf'):
            return {"error": "Only PDF files are allowed."}
        # Specify the directory where files will be saved
       
        file_path = os.path.join(files_folder, pdf_file.filename)
        os.makedirs(files_folder, exist_ok=True)  # Create the directory if it doesn't exist
        
        # Save the PDF file to the specified directory
        file_path = os.path.join(files_folder , pdf_file.filename)
        # Process the PDF file (for example, save it to disk)
        with open(file_path, "wb") as file_object:
            file_object.write(await pdf_file.read())
            
   
        # Extract text from PDF
        text_content = extract_text_from_pdf(file_path)
        processed_file_path = os.path.join(files_folder, f"{pdf_file.filename}.txt")

        # Save the extracted text to a new file
        with open(processed_file_path, "w") as text_file:
            text_file.write(text_content)

        # Optionally delete the original PDF file
        os.remove(file_path)

        response["uploaded_files"].append(pdf_file.filename)
        
    # await process_files();
    return response


def extract_text_from_pdf(file_path):
    document = fitz.open(file_path)
    text = ""
    for page in document:
        text += page.get_text()
    document.close()
    return text

@upload_new_router.get("/")
async def get_upload():
    return {"message": "GET Upload route"}
 