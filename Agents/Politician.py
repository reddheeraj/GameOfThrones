from Person import Person
class Politician (Person):
    def __init__(self, name, personality, party):
        super().__init__(name, personality)
        self.party = party
    
    def getParty(self):
        return self.party
    
    def getPublicRecords(citizens):
        publicRecords = []
        for citizen in citizens:
            publicRecords.append(citizen.getPublicData())
        return publicRecords
    
    def createPost(self):
        '''
        Call the getPublicRecords method to get the public records of all citizens and create a post.
        '''
        pass

