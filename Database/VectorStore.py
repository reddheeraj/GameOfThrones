from Database.ChromaDBConnection import ChromaDBConnection
from logger import logger
from config import CONNECTION_NAME
from langchain_ollama import OllamaEmbeddings
LLM_MODEL = 'llama3.2'
EMBEDDING_MODEL = 'nomic-embed-text'

class Vectorstore:
    def __init__(self, path):
        self.client = ChromaDBConnection(path)
        self.collection = self.client.get_collection(CONNECTION_NAME)

    def add_to_vectorstore(self, ids, vector, metadata, documents):
        self.collection.upsert(ids = ids , embeddings = vector, metadatas = metadata, documents = documents)
        logger.info(f"Added vector to collection: {metadata}")

    def search_vectorstore(self, vector, k):
        results = self.collection.query(vector, n_results=k)
        logger.info(f"Found {len(results)} results")
        return results

    def delete_from_vectorstore(self, metadata):
        self.collection.delete(metadata)
        logger.info(f"Deleted vector from collection: {metadata}")

    def get_embeddings(self):
        # logger.info("Loading embedding model...")
        embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        return embeddings
    
    def queryStore(self, query, k):
        vector = self.get_embeddings().embed_query(query)
        result = self.search_vectorstore(vector, 2)
        return result