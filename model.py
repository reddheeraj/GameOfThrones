from langchain_ollama import ChatOllama
from config import MODEL, GEMINI_API_KEY, GEMINI_MODEL, GROQ_API_KEY, GROQ_MODEL
from google import genai
from langchain_groq import ChatGroq

def get_llm():
    """
    Initialize the language model (either Ollama or Gemini based on configuration).
    """
    print("Initializing LLM...")
    
    # You can toggle between models based on configuration
    if MODEL == "gemini":
        llm = get_gemini_llm()  # Use Gemini model
    elif MODEL == "groq":
        llm = get_groq_llm()  # Use Groq model
    else:
        llm = get_ollama_llm()  # Default to Ollama model
    
    return llm

def get_ollama_llm():
    """
    Initialize and return the Ollama LLM.
    """
    print("Initializing Ollama model...")
    llm = ChatOllama(model=MODEL)
    return llm

def get_groq_llm():
    """
    Initialize and return the Groq LLM.
    """
    print("Initializing Groq model...")
    llm = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL)
    return llm

def get_gemini_llm():
    """
    Initialize and return the Gemini LLM using the Google Gen AI SDK.
    """
    print("Initializing Gemini model...")
    
    # Initialize the Google Gen AI client with the provided API key
    client = genai.Client(api_key=GEMINI_API_KEY)

    return client
    

def request_ollama(prompt):
    """
    Function to request a response from the LLM (Ollama or Gemini based on model configuration).
    """
    llm = get_llm()
    if isinstance(llm, genai.Client): 
        try:
            response = llm.models.generate_content(
                model=GEMINI_MODEL, contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Error generating content from Gemini: {e}")
            return None
    else:
        try:
            res = llm.invoke(prompt)
            return res.content
        except Exception as e:
            print(f"Error generating content from Ollama: {e}")
            return None