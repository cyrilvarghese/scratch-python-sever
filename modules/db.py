# db.py
import chromadb
from chromadb import Settings

# Global variable to hold the persistent client instance
persistent_client = None

def get_db(is_reset=False):
    global persistent_client
    if persistent_client is None:
        persistent_client = chromadb.PersistentClient(
            path="chroma_db",
            settings=Settings(allow_reset=is_reset)
        )
    return persistent_client


