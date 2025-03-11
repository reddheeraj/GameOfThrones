from Agents.Person import Person

class Citizen(Person):
    def __init__(self, name, personality, publicRecord):
        super().__init__(name, personality)
        self.data = publicRecord
    
    def searchPost(query):
        pass

    def getPublicData(self):
        return self.data
    
    def vote(self):
        pass