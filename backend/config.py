import os

LOG_DIR = "logs"
CHROMA_DB_PATH = "chromadb"
SQLITE_DB_PATH = "sqlite"   
PROJECT_DIR = os.getcwd()
PROMPTS_DIR = os.path.join(PROJECT_DIR, "Prompts")
PERSONALITIES_DIR = os.path.join(PROJECT_DIR, "Personalities")
CONNECTION_NAME = "Test"

# MODEL = 'llama3.1'
# MODEL = 'gemini'
MODEL = 'groq'
GEMINI_API_KEY = ''
GEMINI_MODEL = 'gemini-2.0-flash-001'

GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-70b-8192"