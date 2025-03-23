import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from collections import defaultdict
from Agents.Citizen import Citizen
from Agents.Politician import Politician
from Database.VectorStore import VectorStore
from config import PROJECT_DIR
import time
from socket_manager import emit_agent_action

# Global variables to hold the simulation state
citizens = []
politicians = []
vectorStore = None
vote_counts = defaultdict(int)
all_posts = []

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

def initialize_simulation():
    """
    Initialize the simulation environment.
    """
    global citizens, politicians, vectorStore
    citizen_path = os.path.join(PROJECT_DIR, "Personalities", "Citizens")
    politician_path = os.path.join(PROJECT_DIR, "Personalities", "Politicians")
    citizens = load_citizens(citizen_path)
    politicians = load_politicians(politician_path)
    vectorStore = VectorStore('Test')

def politicians_create_posts():
    global all_posts
    for politician in politicians:
        action = f"{politician.name} created a post."
        emit_agent_action(action)
        politician.createPost(citizens, vectorStore, 1)
        posts = [(doc, meta) for doc, meta in vectorStore.get_all_documents()]
        all_posts.extend(posts)
        time.sleep(2)

def citizens_decide_votes():
    global vote_counts
    vote_counts = defaultdict(int)
    for citizen in citizens:
        vote = citizen.vote(vectorStore, politicians)
        citizen.vote_decision = vote
        action = f"{citizen.name} voted for {vote}."
        emit_agent_action(action)
        if citizen.vote_decision != "No Vote":
            vote_counts[citizen.vote_decision] += 1
        time.sleep(2)

def run_simulation_step():
    """
    Run one step of the simulation.
    """
    politicians_create_posts()
    citizens_decide_votes()

def run_simulation_regularly():
    """
    Run the simulation regularly.
    """
    while True:
        politicians_create_posts()
        citizens_decide_votes()
        time.sleep(10)

def get_simulation_state():
    """
    Get the current state of the simulation.
    """
    global vote_counts
    citizen_states = [{"name": c.name, "vote": c.vote_decision, "memory": c.recall()} for c in citizens]
    politician_states = [{"name": p.name, "party": p.party, "memory": p.recall()} for p in politicians]
    return {
        "citizens": citizen_states,
        "politicians": politician_states,
        "vote_counts": dict(vote_counts),
    }

def get_all_posts():
    """
    Get all social media posts.
    """
    global all_posts
    return [{"content": post[0], "metadata": post[1]} for post in all_posts]
