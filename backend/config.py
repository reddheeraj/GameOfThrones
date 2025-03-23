import os

LOG_DIR = "logs"
CHROMA_DB_PATH = "chromadb"
SQLITE_DB_PATH = "sqlite"   
PROJECT_DIR = os.getcwd()
PROMPTS_DIR = os.path.join(PROJECT_DIR, "Prompts")
PERSONALITIES_DIR = os.path.join(PROJECT_DIR, "Personalities")
CONNECTION_NAME = "GOT"

# MODEL = 'llama3.1'
# MODEL = 'gemini'
MODEL = 'groq'
GEMINI_API_KEY = 'AIzaSyApw1u5HtDcdOe0P_2PAjBuXH61WOvCOFc'
# AIzaSyDKuKNsUejkxTBFG17uGT42tYQ-R2QkKz0
GEMINI_MODEL = 'gemini-2.0-flash-001'

GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-70b-8192"