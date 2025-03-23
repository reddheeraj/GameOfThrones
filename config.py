import os

LOG_DIR = "logs"
CHROMA_DB_PATH = "chromadb"
SQLITE_DB_PATH = "sqlite"
PROJECT_DIR = os.getcwd()
PROMPTS_DIR = os.path.join(PROJECT_DIR, "Prompts")
PERSONALITIES_DIR = os.path.join(PROJECT_DIR, "Personalities")
CONNECTION_NAME = "GOT"

MODEL = 'llama3.2'