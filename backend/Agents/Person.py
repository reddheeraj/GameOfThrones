from string import Template
import os

class Memory:
    def __init__(self):
        self.data = []

    def add(self, event):
        self.data.append(event)

    def recall(self):
        return self.data
    
class Person:
    def __init__(self, name, personality, publicRecord):
        self.name = name
        self.personality = personality
        self.publicRecord = publicRecord
        self.memory = Memory()
    
    def getName(self):
        return self.name
    
    def getPublicData(self):
        return self.publicRecord

    def _load_prompt(self, filename: str) -> Template:
        """
        Load a prompt template from file.
        """
        path = os.path.join(os.getcwd(), 'Prompts', filename)
        with open(path, 'r') as file:
            content = file.read()
        return Template(content)
    
    def recall(self):
        """
        Recall the memory of the person.
        """
        
        return self.memory.recall()
    
    def remember_instance(self, event):
        """
        Add an event to the memory of the person.
        """
        self.memory.add(event)
