from ChromaDBConnection import ChromaDBConnection
from logger import logger
from config import CONNECTION_NAME

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