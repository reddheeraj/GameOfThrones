class Person:
    def __init__(self, name, personality, publicRecord):
        self.name = name
        self.personality = personality
        self.publicRecord = publicRecord
    
    def getName(self):
        return self.name
    
    def getPublicData(self):
        return self.publicRecord