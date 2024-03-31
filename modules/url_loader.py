from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import BSHTMLLoader
from html2text import html2text
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_transformers import Html2TextTransformer
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from modules.youtube_loader import write_video_content_to_file
from dotenv import load_dotenv
load_dotenv()
import chromadb
from chromadb.config import Settings
from urllib.parse import urlparse 
import json
from urllib.parse import urlparse
from datetime import datetime
from modules.url_mapping import generate_filename

documents = []
splitter = RecursiveCharacterTextSplitter(chunk_size=700)
embeddings= OpenAIEmbeddings(model="text-embedding-3-large")



def extract_website_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.split('.')[-2]  # Extract the second-to-last part of the netloc
    return domain

# not used anymore 
# def web_url_loader(urls):
#     print("Processing web URLs:")
#     loader = WebBaseLoader(urls)
#     docs =  loader.load()
#     html2text = Html2TextTransformer()
#     docs_transformed = html2text.transform_documents(docs)
#     split_docs = splitter.split_documents(docs_transformed)
 
#     print("Processing web urls complete")

     
#     print("Document count from URLs:", len(split_docs))

#     persistent_client = chromadb.PersistentClient(path="chroma_db")

#     langchain_chroma = Chroma.from_documents( split_docs, embeddings ,collection_name="ux-research-base", persist_directory="chroma_db")
 
#     print("Document count added :", langchain_chroma._collection.count())

def is_youtube_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return "youtube.com" in domain or "youtu.be" in domain

# def generate_filename(url):
#     # Extract the last part of the URL after the slash
#     path_parts = urlparse(url).path.split('/')
#     website_name = extract_website_name(url)
#     last_part = path_parts[-1] if path_parts[-1] else path_parts[-2]  # Get the last non-empty part
#     # Convert the current date and time to the specified format
#     formatted_date = datetime.now().strftime('%d_%m')
#     # Construct the filename using the extracted part and formatted date
#     filename = f"{website_name}_{formatted_date}_{last_part}.txt"
#     return filename


def web_url_to_text(urls):
    print("Processing web URLs:")
    for index, url in enumerate(urls):
        try:
            if is_youtube_url(url):
               write_video_content_to_file(url);
            else:
                request_headers = {
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                response = requests.get(url,headers=request_headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    text = soup.get_text()
                    filename =generate_filename(url)
                    file_path = os.path.join("../python-server/files", filename)

                    # Create the directory if it doesn't exist
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(text)
                    print(f" saved  url {index} to {filename}")
                else:
                    print(f"Failed to retrieve content from {url}: Status code {response.status_code}")
        except Exception as e:
            print(f"Error processing {url}: {e}")

    print("Processing web URLs complete")