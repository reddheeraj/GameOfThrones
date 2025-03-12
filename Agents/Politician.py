from Agents.Person import Person
from model import request_ollama
from duckduckgo_search import DDGS
import json
import requests
from bs4 import BeautifulSoup
from Database.SocialMedia import SocialMedia
from Database.ChromaDBConnection import ChromaDBConnection
from datetime import datetime
import re

class Politician (Person):
    def __init__(self, name, personality, party, publicRecord):
        super().__init__(name, personality, publicRecord)
        self.party = party
    
    def getPublicRecords(self, citizens):
        publicRecords = []
        for citizen in citizens:
            publicRecords.append(citizen.getPublicData())
        return publicRecords
    
    def searchCurrectAffairs(self, queries, num_results=5):
        ddgs = DDGS()
        news_results = {}
        
        for query in queries:
            search_results = list(ddgs.news("Latest News "+query, max_results=num_results))
            # news_results[query] = [result["body"] for result in search_results]
            news_results[query] = search_results
        return news_results

    def getCurrentAffairs(self,publicRecords):
        publicRecords_str = ""
        for i, record in enumerate(publicRecords):
            publicRecords_str = f'Citizen {i}: ' + record + '\n'
        prompt = f"""
        Given the following public records of citizens, give me a single list of {len(publicRecords)} distinct and extensive search queries which
        can be used to search for major recent news related to their occupations and interests.:
        
        {publicRecords_str}
        
        The queries should be specific and focus on major news related to their occupations and interests.
        DO NOT include any other unwanted text like: ' Here are five search queries ...'.
        STRICT OUTPUT FORMAT: [query1, query2, query3, query4, query5]
        """
        results = {}
        for i in range(5):
            try:
                response = request_ollama(prompt)
                # print(response["message"]['content'])
                queries = eval(response)  # Convert response into a Python list
                results = self.searchCurrectAffairs(queries, 3)
                break
            except Exception as e:
                print(e)
                print(response["message"]['content'])
        return results

    def summarize(self, text):
        prompt = f"""
        Given the following text, summarize it into a single paragraph:

        {text}

        DO NOT include any other unwanted text like: 'Here is the summary ...'.
        """

        response = request_ollama(prompt)
        return response  # Return the summary

    def scrape(self, currentAffairs):

        def get_full_article(url):
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                article_body = soup.find("article")
                if not article_body:
                    article_body = soup.find("div", class_="entry-content")
                if article_body:
                    return True, article_body.get_text()
            
            return False, "Full article could not be extracted."
        
        scraped_affairs = {}
        for key in list(currentAffairs.keys()):
            x_list = []
            for article in currentAffairs[key]:
                url = article['url']
                status, full_article = get_full_article(url)
                if status:
                    x_list.append(self.summarize(full_article))
                else:
                    x_list.append(article['body'])
            scraped_affairs[key] = x_list
        
        return scraped_affairs

    def createPost(self, citizens, vectorStore, num = 1):
        '''
        Call the getPublicRecords method to get the public records of all citizens and create a post.
        '''
        publicRecords = self.getPublicRecords(citizens)
        currentAffairs = self.getCurrentAffairs(publicRecords)
        # json.dump(currentAffairs, open("currentAffairs.json", "w"), indent=4)
        summarized_affairs = self.scrape(currentAffairs)
        # print(summarized_affairs)
        # with open("summarizedAffairs.json", "w") as f:
        #     json.dump(summarized_affairs, f, indent=4)
        
        summarized_affairs_str = ""

        for key in summarized_affairs.keys():
            if len(summarized_affairs[key]) == 0:
                continue
            summarized_affairs_str += f"{key}:\n"
            for i, summary in enumerate(summarized_affairs[key]):
                summarized_affairs_str += f"Article {i+1}: {summary}\n"
            summarized_affairs_str += "\n"
        
        publicRecords_str = ""
        for i, record in enumerate(publicRecords):
            publicRecords_str = f'Citizen {i}: ' + record + '\n'
        
        personality = self.personality
        print('-'*50)
        prompt = f"""
        {personality}

        These are the citizens who will vote for you in the upcoming elections.

        {publicRecords_str}

        These are summarized latest news articles related to the citizens:
        
        {summarized_affairs_str}

        Create exactly {num} unique social media post which showcases polcies or idealogies 
        that you wish to implement if you win the elections. The posts should have a minimum of 50 words.
        You are goal is to attract all citizens to vote for you.
        Return a SINGLE json object with keys as numbers: 1,2,3...

        ### Example of a correct response:
        {{
            1: String1,
            2: String2,
            .
            .
            .
        }}

        DO NOT return any other unwanted text like: 'Here is the post ...' or 'This social media post showcases...' or 'Feel free to modify or expand on this post...'.
        """
        posts=[]
        for i in range(5):
            try:
                response = request_ollama(model='llama3.1', messages=[{"role": "user", "content": prompt}])
                json_pattern = re.compile(r'\{(?:[^{}]|"(?:\\.|[^"\\])*")*\}', re.DOTALL)
                json_match = json_pattern.search(response)
                if json_match:
                    json_str = json_match.group(0).strip()
                    posts = json.loads(json_str)
                    break
                else:
                    print(response)
            except Exception as e:
                print(e)
                print(response)
        print('+'*50)
        with open(f"posts{self.name}.json", "w") as f:
            json.dump(posts, f, indent=4)
        vector_posts = []
        post_str=[]
        embeddings = vectorStore.get_embeddings()
        for key in posts.keys():
            vector_posts.append(embeddings.embed_query(posts[key]))
            post_str.append(posts[key])
        dt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        ids = [dt + "_" + str(i) for i in range(len(vector_posts))]
        metadata = [{"name": self.name, "date_time": dt}] * len(vector_posts)
        vectorStore.add_to_vectorstore(ids = ids, vector = vector_posts, metadata = metadata, documents = post_str)