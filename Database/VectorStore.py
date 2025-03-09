from ChromaDBConnection import ChromaDBConnection
from logger import logger
from config import CONNECTION_NAME

class Vectorstore:
    def __init__(self, path):
        self.client = ChromaDBConnection(path)
        self.connection = self.client.get_collection(CONNECTION_NAME)

    def add_to_vectorstore(self, vector, metadata):
        self.connection.insert(vector, metadata=metadata)
        logger.info(f"Added vector to collection: {metadata}")

    def search_vectorstore(self, vector, k):
        results = self.connection.query(vector, k=k)
        logger.info(f"Found {len(results)} results")
        return results

    def delete_from_vectorstore(self, metadata):
        self.connection.delete(metadata)
        logger.info(f"Deleted vector from collection: {metadata}")
    
