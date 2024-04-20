import chromadb
from  dotenv import load_dotenv
from modules.file_processor import process_files
from modules.url_loader import web_url_to_text  # Adjust the path accordingly
from modules.file_handler import read_data_from_file
from config import DB_NAME
import os
load_dotenv()

def clear_processed_files():
    try:
        os.remove("../python-server/files/processed_files.txt")
        print("Processed files cleared successfully.")
    except FileNotFoundError:
        print("Processed files not found. No action taken.")

async def setup_chroma(is_reset=False):
    try:    
        # persisten_client= chromadb.PersistentClient(path="chroma_db",settings=Settings(allow_reset=is_reset))
        chroma_client = chromadb.HttpClient(host='localhost', port=3001)
        if is_reset:
            print("client Reset ",chroma_client.reset());
        collection = chroma_client.get_or_create_collection(name=DB_NAME)
        print("collection created with docs:",collection.count())
        if is_reset:
            urls = read_data_from_file();
            print("Web URLs processing ----url found:",len(urls))
            if read_data_from_file():
                web_url_to_text(read_data_from_file());
            clear_processed_files();
            await process_files();
        
            print("Web URLs processing complete ----")
    except Exception as e:
        print("An error occurred:", str(e))
    
 