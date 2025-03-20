import ollama
from config import MODEL

def request_ollama(prompt):
    response = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return response['message']['content']