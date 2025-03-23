import os
import json
from Agents.Person import Person
from model import request_ollama
from typing import List
from logger import logger
from config import PROMPTS_DIR
from Database.VectorStore import VectorStore

class Citizen(Person):
    def __init__(self, name: str, personality: str, publicRecord: str) -> None:
        """
        Initialize a Citizen object.

        Args:
            name (str): Name of the citizen.
            personality (str): Personality type or description.
            public_record (str): Public record data for the citizen.
        """
        super().__init__(name, personality, publicRecord)
        self.vote_decision = None
    
    def getPublicRecords(self, politicians: List[Person]) -> List[str]:
        """
        Get public records from politicians.

        Args:
            politicians (List[Person]): List of politician objects.

        Returns:
            List[str]: List of public records from politicians.
        """
        logger.info(f"{self.name} is retrieving public records from politicians.")
        return [politician.getPublicData() for politician in politicians]

    def searchPost(self, vectorStore: VectorStore, politicians: List[Person], k: int = 5) -> List[str]:
        """
        Search for relevant posts from the vector store using generated queries.

        Args:
            vector_store (VectorStore): Vector store instance for querying posts.
            politicians (List[Person]): List of politician objects.
            k (int): Number of search results to return.

        Returns:
            List[str]: List of search results.
        """
        logger.info(f"{self.name} is initiating a post search...")

        # Get public records from politicians
        publicRecords = self.getPublicRecords(politicians)
        if not publicRecords:
            logger.error("No public records found from politicians.")
            return []
    
        logger.info(f"Public records: {publicRecords}")

        prompt_path = os.path.join(PROMPTS_DIR, 'searchPost_prompt.txt')
        
        # Create the search prompt
        prompt = self._load_prompt(prompt_path).substitute(
            personality=self.personality,
            publicRecords="\n".join(publicRecords)
        )
        logger.debug(f"Generated Prompt: {prompt}")

        # Generate query using LLM
        try:
            response = request_ollama(prompt)
            logger.info(f"LLM Response: {response}")
        except Exception as e:
            logger.error(f"Failed to get LLM response: {e}")
            return []

        # Search vector store using the generated query
        try:
            results = vectorStore.queryStore(response, k)
            results = results['documents'][0]
            # print("RESULTS: ", results)
            logger.info(f"Retrieved {len(results)} results from vector store.")
            return results
        except Exception as e:
            logger.error(f"Vector store query failed: {e}")
            return []
        
    def vote(self, vectorStore: VectorStore, politicians: List[Person]) -> str:
        """
        Citizen decides to vote based on the relevance of retrieved posts.

        Args:
            vectorStore (VectorStore): Vector store for retrieving politician posts.
            politicians (List[Person]): List of politician objects.

        Returns:
            str: Name of the politician voted for or 'No Vote'.
        """
        logger.info(f"{self.name} is deciding on a vote...")

        # Search for relevant posts from politicians
        search_results = self.searchPost(vectorStore, politicians, k=5)
        if not search_results:
            logger.info(f"{self.name} could not find any relevant posts.")
            return "No Vote"

        logger.debug(f"Search Results: {search_results}")

        # Build prompt for decision making
        prompt_template = os.path.join(PROMPTS_DIR, 'decision_making_prompt.txt')

        prompt = self._load_prompt(prompt_template).substitute(
            personality=self.personality,
            publicRecord=self.getPublicRecords(politicians),
            posts="\n\n".join(search_results),
            memories=self.recall()
        )

        logger.debug(f"Generated Decision Prompt: {prompt}")

        # Use LLM to make a decision
        try:
            resObj = request_ollama(prompt).strip()
            resObj = json.loads(resObj.strip("```json").strip("```"))
            # print("RESOBJ: ", resObj)
            response, because = resObj["politician"], resObj["because"]
            logger.info(f"{self.name} decided to vote for: {response}")
        except Exception as e:
            logger.error(f"Failed to get decision from LLM: {e}")
            return "No Vote"
        
        # Validate if the response is a known politician
        politician_names = [politician.name for politician in politicians]
        if response in politician_names:
            logger.info(f"{self.name} voted for {response}")
            self.vote_decision = response
            self.remember_instance({"vote": response, "because": because})
            logger.info(f"CITIZEN: {self.name} voted for {response} because {because}")
            return response
        else:
            logger.info(f"{self.name} did not vote for any politician.")
            self.remember_instance({"vote": "No Vote", "because": because})
            logger.info(f"CITIZEN: {self.name} chose to not vote because {because}")
            return "No Vote"