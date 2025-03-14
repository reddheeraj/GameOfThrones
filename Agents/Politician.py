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
import os
from string import Template

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
        prompt_path = os.path.join(os.getcwd(),'Prompts','web_prompt.txt')
        with open(prompt_path, 'r') as f:
            prompt_template = f.read()
        
        template = Template(prompt_template)
        prompt = template.substitute(len_publicRecords=len(publicRecords), publicRecords_str=publicRecords_str)
        results = {}
        for i in range(5):
            try:
                response = request_ollama(prompt)
                queries = eval(response)  # Convert response into a Python list
                results = self.searchCurrectAffairs(queries, 3)
                break
            except Exception as e:
                print(e)
                print(response["message"]['content'])
        return results

    def summarize(self, text):
        prompt_path = os.path.join(os.getcwd(),'Prompts','summary_prompt.txt')
        with open(prompt_path, 'r') as f:
            prompt_template = f.read()
        
        template = Template(prompt_template)
        prompt = template.substitute(text=text)
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
        prompt_path = os.path.join(os.getcwd(),'Prompts','post_prompt.txt')
        with open(prompt_path, 'r') as f:
            prompt_template = f.read()
        
        template = Template(prompt_template)
        prompt = template.substitute(personality=personality, publicRecords_str=publicRecords_str, summarized_affairs_str=summarized_affairs_str, num=num)
        posts=[]
        response = ""
        for i in range(5):
            try:
                response = request_ollama(prompt)
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