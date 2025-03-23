from langchain_ollama import ChatOllama, OllamaEmbeddings
from config import MODEL

def get_llm():
    print("Initializing LLM...")
    llm = ChatOllama(model=MODEL)
    return llm

def request_ollama(prompt):
    llm = get_llm()
    res = llm.invoke(prompt)
    return res.content