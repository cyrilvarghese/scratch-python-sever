import os
# unique_docs.py
from  modules.url_mapping import get_original_url
from urllib.parse import quote

def extract_unique_documents(docs):
    """
    Extracts unique documents based on their page_content from a nested list of documents and enriches
    the document with its original URL source if available.

    Args:
        docs (list): A nested list of documents.
        
    Returns:
        tuple: A tuple containing a list of unique documents and a list of dictionaries with detailed content information.
    """

    unique_contents = set()
    unique_docs = []
    unique_content_details = []  # List to hold dictionaries of content details
    files_folder = "files"  # Path to the 'files' folder
    server_url = "http://localhost:8000"

    for doc in docs:
        if doc.page_content not in unique_contents:
            # Extract file name from the document's source metadata
            file_name = os.path.basename(doc.metadata['source'])
            # Assuming get_original_url is a function that retrieves the original URL from a filename
            url_source = get_original_url(file_name)
            file_path = os.path.join(files_folder, file_name)
            file_source= f"{server_url}/{quote(file_path)}"

            
            # Update doc metadata with URL source
            doc.metadata['url_source'] = url_source

            # Append the document to the list of unique documents
            unique_docs.append(doc)
            # Add the content's details to the unique_content_details list
            unique_content_details.append({
                "page_content": doc.page_content,
                "file_source":file_source,
                "url_source": url_source
            })

            # Add the page_content to the set of unique contents
            unique_contents.add(doc.page_content)
    
    return unique_docs, unique_content_details