import json
from config import PROJECT_DIR
import os
from Agents.Citizen import Citizen
from Agents.Politician import Politician
from Database.VectorStore import Vectorstore



def load_citizens(path):
    citizens = []
    for citizen in os.listdir(path):
        with open(os.path.join(path, citizen), "r") as f:
            file = json.load(f)
            citizen = Citizen(file["Name"], file["Personality"], file["PublicRecord"])
            citizens.append(citizen)
    return citizens

def load_politicians(path):
    politicians = []
    for politician in os.listdir(path):
        with open(os.path.join(path, politician), "r") as f:
            file = json.load(f)
            politician = Politician(file["Name"], file["Personality"], file["Party"], file["PublicRecord"])
            politicians.append(politician)
    return politicians


def simulate():
    citizen_path = os.path.join(PROJECT_DIR, "Personalities", "Citizens")
    politician_path = os.path.join(PROJECT_DIR, "Personalities", "Politicians")

    citizens = load_citizens(citizen_path)
    politicians = load_politicians(politician_path)
    
    vectorStore = Vectorstore('Test')
    for politician in politicians:
        politician.createPost(citizens, vectorStore, 5)
    

    citizens[0].searchPost(vectorStore, politicians, 5)


simulate()