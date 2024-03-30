
# unique_docs.py

def extract_unique_documents(docs):
    """
    Extracts unique documents based on their page_content from a nested list of documents.
    
    Args:
        docs (list): A nested list of documents.
        
    Returns:
        tuple: A tuple containing a list of unique documents and a list of unique page contents.
    """
    unique_contents = set()
    unique_docs = []
    for doc in docs:
        if doc.page_content not in unique_contents:
            unique_docs.append(doc)
            unique_contents.add(doc.page_content)
    
    unique_contents = list(unique_contents)
    
    return unique_docs, unique_contents