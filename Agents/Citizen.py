from Agents.Person import Person
from model import request_ollama
from Database.VectorStore import Vectorstore

class Citizen(Person):
    def __init__(self, name, personality, publicRecord):
        super().__init__(name, personality, publicRecord)
    
    def getPublicRecords(self, politicians):
        publicRecords = []
        for politician in politicians:
            publicRecords.append(politician.getPublicData())
        return publicRecords

    def searchPost(self, vectorStore, politicians, k):
        publicRecords = self.getPublicRecords(politicians)
        personality = self.personality
        prompt = f"""
        You are a citizen of a constituency.
        {personality}
        Given the following public records of politicians:

        {publicRecords}

        Politicians have shared posts on social media. Generate a very simple search query with 3 words that will help you find the most relevant post based on your interests or idealogies.
        Return a single string.
        DO NOT include any other unwanted text like: 'Here is the search query ...'.
        """
        
        response = request_ollama(prompt)
        print(f"Response: {response}")
        results = vectorStore.queryStore(response, k)

        print(results)
    
    def vote(self):
        pass