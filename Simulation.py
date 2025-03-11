import json
from config import PROJECT_DIR
import os
from Agents.Citizen import Citizen
from Agents.Politician import Politician
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
    print(citizens)
    politicians[0].createPost(citizens)

simulate()