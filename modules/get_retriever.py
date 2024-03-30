from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
from chromadb.config import Settings
load_dotenv()
from langchain_community.embeddings import CohereEmbeddings
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.chat_models import ChatCohere
from langchain.retrievers.document_compressors import CohereRerank
 

embeddings = OpenAIEmbeddings(model= "text-embedding-3-large")
# embeddings = CohereEmbeddings(model="embed-english-light-v3.0")
chroma_client = chromadb.HttpClient(host='localhost', port=3001)

 
def get_retriever(num_of_results):
    try:
        collection = chroma_client.get_collection(name='ux-research-base')
        print("---from api")
        print(collection)
        if collection:
            persistent_client = chromadb.PersistentClient(path="chroma_db",settings=Settings(allow_reset=True))
            langchain_chroma= Chroma(client=persistent_client, embedding_function=embeddings,collection_name="ux-research-base")
            # retriever = langchain_chroma.as_retriever(  search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5,"k": num_of_results})
            retriever = langchain_chroma.as_retriever( search_kwargs={"k": num_of_results})
          
            # cohere_rerank = CohereRerank()
            # compression_retriever = ContextualCompressionRetriever(
            #         base_compressor=cohere_rerank, 
            #         base_retriever=retriever
            #     )
            # return compression_retriever
            return retriever
    except Exception as e:
        print('Error retrieving documents:', e)

# Example usage:
# retriever = await get_retriever()
# relevant_docs = await retriever.get_relevant_documents(question)