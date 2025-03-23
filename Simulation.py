import json
from config import PROJECT_DIR
import os
from Agents.Citizen import Citizen
from Agents.Politician import Politician
from Database.VectorStore import VectorStore
from collections import defaultdict
import time



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


def simulate(n_iterations=5):
    citizen_path = os.path.join(PROJECT_DIR, "Personalities", "Citizens")
    politician_path = os.path.join(PROJECT_DIR, "Personalities", "Politicians")

    citizens = load_citizens(citizen_path)
    politicians = load_politicians(politician_path)

    
    vectorStore = VectorStore('Test')

    # for politician in politicians:
    #     politician.createPost(citizens, vectorStore, 5)
    
    for iteration in range(n_iterations):
        print(f"--- Iteration {iteration + 1} ---")

        # Citizens decide their votes based on posts and updates
        for citizen in citizens:
            vote = citizen.vote(vectorStore, politicians)
            citizen.vote_decision = vote
            time.sleep(2)
            

        # Tally votes for politicians
        vote_counts = defaultdict(int)
        for citizen in citizens:
            if citizen.vote_decision != "No Vote":
                vote_counts[citizen.vote_decision] += 1

        # Print current vote status
        print(f"Current vote counts: {dict(vote_counts)}")

        print("\n--- End of Iteration ---\n")

    print("\n--- Final Vote Counts ---")
    final_vote_counts = defaultdict(int)
    for citizen in citizens:
        if citizen.vote_decision != "No Vote":
            final_vote_counts[citizen.vote_decision] += 1
    print(f"Final vote counts: {dict(final_vote_counts)}")

    winner = max(final_vote_counts, key=final_vote_counts.get, default=None)
    if winner:
        print(f"\nWinner: {winner}")
    else:
        print("\nNo one won the election.")


simulate()