import json
from config import PROJECT_DIR
import os
from Agents.Citizen import Citizen
from Agents.Politician import Politician
from Database.VectorStore import Vectorstore

def queryStore(vectorStore):
    query = input("Enter query: ")
    vector = vectorStore.get_embeddings().embed_query(query)
    result = vectorStore.search_vectorstore(vector, 2)
    print(result)

def simulate():
    citizen_path = os.path.join(PROJECT_DIR, "Personalities", "Citizens")
    politician_path = os.path.join(PROJECT_DIR, "Personalities", "Politicians")

    citizens = []
    politicians = []
    for citizen in os.listdir(citizen_path):
        with open(os.path.join(citizen_path, citizen), "r") as f:
            file = json.load(f)
            citizen = Citizen(file["Name"], file["Personality"], file["PublicRecord"])
            citizens.append(citizen)
    for politician in os.listdir(politician_path):
        with open(os.path.join(politician_path, politician), "r") as f:
            file = json.load(f)
            politician = Politician(file["Name"], file["Personality"], file["Party"])
            politicians.append(politician)
    vectorStore = Vectorstore('Test')
    for politician in politicians:
        politician.createPost(citizens, vectorStore, 5)
    queryStore(vectorStore)

simulate()