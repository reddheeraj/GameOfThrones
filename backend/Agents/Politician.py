import json
from logger import logger
import re
from datetime import datetime
from typing import List, Dict, Any

import requests
from bs4 import BeautifulSoup
# from duckduckgo_search import DDGS
from googlesearch import search

from Agents.Person import Person
from model import request_ollama
from Database.VectorStore import VectorStore


class Politician(Person):
    def __init__(self, name: str, personality: str, party: str, public_record: str):
        super().__init__(name, personality, public_record)
        self.party = party
    
    def getMemory(self) -> None:
        """
        Get memory from the vector store.
        """
        logger.info(f"Getting memory for {self.name}...")
        # -------------------------------------------------------------------------
        # -------------------------------------------------------------------------
        # -------------------------------------------------------------------------
        return VectorStore('Test').get_content_of_person(self.name)
        # -------------------------------------------------------------------------
        # -------------------------------------------------------------------------
        # -------------------------------------------------------------------------
    
    def getPublicRecords(self, citizens: List[Person]) -> List[str]:
        """
        Extract public records from citizens.
        """
        logger.info("Extracting public records from citizens...")
        return [citizen.getPublicData() for citizen in citizens]
    
    def searchCurrectAffairs(self, queries: List[str], num_results: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search current news using DuckDuckGo.
        """
        logger.info(f"Searching current affairs for {queries}")

        news_results = {}
        
        for query in queries:
            try:
                search_results = search(f"Latest News {query}", num_results=num_results)
                news_results[query] = search_results
            except Exception as e:
                logger.error(f"Failed to fetch news for query '{query}': {e}")
        
        return news_results

    def getCurrentAffairs(self, publicRecords: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate search queries based on public records and search for related news.
        """
        logger.info("Generating search queries based on public records...")
        publicRecords_str = "\n".join([f"Citizen {i}: {record}" for i, record in enumerate(publicRecords)])


        # try:
        prompt = self._load_prompt("web_prompt.txt").substitute(
            len_publicRecords=len(publicRecords),
            publicRecords_str=publicRecords_str
        )
        response = request_ollama(prompt)
        print("RESPONSE: ", response)
        # queries = eval(response)  # Convert string response into list
        queries = self.extract_code_blocks(response)
        return self.searchCurrectAffairs(queries)
        # except Exception as e:
        #     logger.error(f"Failed to generate queries from public records: {e}")
        #     return {}

    def extract_code_blocks(self, text: str) -> list:
        code_blocks = re.findall(r"```(.*?)```", text, re.DOTALL)
        return code_blocks

    def summarize(self, text: str) -> str:
        """
        Summarize large text using the model.
        """
        try:
            prompt = self._load_prompt("summary_prompt.txt").substitute(text=text)
            return request_ollama(prompt)
        except Exception as e:
            logger.error(f"Failed to summarize text: {e}")
            return text

    def scrape(self, currentAffairs: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Scrape full articles and summarize them.
        """
        logger.info("Scraping full articles and summarizing...")

        def scrape_url(url: str) -> str:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            }
            
            try:
                print(f"Fetching URL: {url}")
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")
                
                # Find main content (for Wikipedia, it's usually inside <p> tags)
                paragraphs = soup.find_all('p')
                body_text = ' '.join(p.get_text(strip=True) for p in paragraphs)
                
                if not body_text:
                    logger.info(f"No body content found at {url}")
                    return "No content available."
        
                # Limit the length to avoid huge text output
                # trimmed_text = body_text[:max_length] + ("..." if len(body_text) > max_length else "")
                logger.info(f"Successfully scraped content from {url}")

                return body_text
    
            except requests.RequestException as e:
                logger.info(f"Request error while fetching {url}: {e}")
            except Exception as e:
                logger.info(f"Error processing {url}: {e}")
            
            return ""
        
        summarized_affairs = {}
        for query, generator in currentAffairs.items():
            summaries = []
            articles = list(generator)
            for article in articles:
                url = article
                body = scrape_url(url)
                print("BODY: ", body[:200])
                summary = self.summarize(body) if body else "No content available"
                summaries.append(summary)
            summarized_affairs[query] = summaries

        return summarized_affairs

    def createPost(self, citizens: List[Person], vectorStore: VectorStore, num: int = 1) -> None:
        """
        Create social media post based on current affairs and public records.
        Call the getPublicRecords method to get the public records of all citizens and create a post.
        """
        logger.info(f"Creating post for {self.name}...")
        prevPosts = self.getMemory()
        publicRecords = self.getPublicRecords(citizens)
        currentAffairs = self.getCurrentAffairs(publicRecords)
        summarized_affairs = self.scrape(currentAffairs)
        
        summarized_affairs_str = "\n".join(
            f"{key}:\n" + "\n".join(f"Article {i + 1}: {summary}" for i, summary in enumerate(summaries))
            for key, summaries in summarized_affairs.items()
        )
        
        publicRecords_str = "\n".join([f"Citizen {i}: {record}" for i, record in enumerate(publicRecords)])
        
        prompt = self._load_prompt("post_prompt.txt").substitute(
            personality=self.personality,
            publicRecords_str=publicRecords_str,
            summarized_affairs_str=summarized_affairs_str,
            prevPosts=prevPosts,
            num=num
        )

        try:
            response = request_ollama(prompt)
            posts = self._extract_json(response)

            logger.info("POSTS:")
            logger.info("---------------------------------------")
            logger.info(posts)

            self._save_posts(posts)
            self._store_posts(vectorStore, posts)
        except Exception as e:
            logger.error(f"Failed to create post: {e}")
    
    def _extract_json(self, response: str) -> Dict[str, str]:
        """
        Extract JSON content from the model response.
        """
        # try:
        json_pattern = re.compile(r'\{(?:[^{}]|"(?:\\.|[^"\\])*")*\}', re.DOTALL)
        json_match = json_pattern.search(response)
        if json_match:
            json_str = json_match.group(0).strip()
            return json.loads(json_str)
        logger.warning("No valid JSON found in response.")
        # except Exception as e:
        #     logger.error(f"Failed to extract JSON: {e}")
        # return {}

    def _save_posts(self, posts: Dict[str, str]) -> None:
        """
        Save posts to file.
        """
        with open(f"posts_{self.name}.json", "w") as file:
            json.dump(posts, file, indent=4)
        logger.info("Saved posts to file.")

    def _store_posts(self, vector_store: VectorStore, posts: Dict[str, str]) -> None:
        """
        Store posts into the vector database.
        """
        embeddings = vector_store.get_embeddings()
        post_vectors = [embeddings.embed_query(content) for content in posts.values()]
        dt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        ids = [f"{dt}_{i}" for i in range(len(post_vectors))]
        metadata = []
        for content in posts.values():
            metadata.append({"name": self.name, "date_time": dt, "content": content})
        vector_store.add_to_vectorstore(ids=ids, vector=post_vectors, metadata=metadata, documents=list(posts.values()))
        logger.info("Stored posts in vector database.")