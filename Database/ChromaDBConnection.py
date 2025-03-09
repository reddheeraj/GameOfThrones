# Singleton class to manage connection to ChromaDB

import chromadb
from logger import logger
from chromadb.config import Settings

class ChromaDBConnection:
    _instance = None

    def __new__(cls, path):
        if cls._instance is None:
            logger.info("Creating new ChromaDB connection...")
            cls._instance = super(ChromaDBConnection, cls).__new__(cls)
            cls._instance.client = chromadb.PersistentClient(path=path, settings=Settings(anonymized_telemetry=False))
        return cls._instance

    def get_collection(self, name):
        logger.info(f"Accessing collection: {name}")
        collection = self.client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})
        logger.info(f"Collection size: {collection.count()}")
        return collection