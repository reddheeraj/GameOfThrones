import ollama

MODEL = 'llama3.1'

def request_ollama(prompt):
    response = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return response['message']['content']