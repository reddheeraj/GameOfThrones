from string import Template
import os


class Person:
    def __init__(self, name, personality, publicRecord):
        self.name = name
        self.personality = personality
        self.publicRecord = publicRecord
    
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