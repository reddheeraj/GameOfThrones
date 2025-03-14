from Agents.Person import Person
from model import request_ollama
from Database.VectorStore import Vectorstore
import os
from string import Template

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
        prompt_path = os.path.join(os.getcwd(),'Prompts','searchPost_prompt.txt')
        with open(prompt_path, 'r') as f:
            prompt_template = f.read()
        
        template = Template(prompt_template)
        prompt = template.substitute(personality=personality, publicRecords=publicRecords)
        
        response = request_ollama(prompt)
        print(f"Response: {response}")
        results = vectorStore.queryStore(response, k)

        print(results)
    
    def vote(self):
        pass