from logger import logger
import sqlite3

class SocialMedia:
    # SQL DB connection
    _instance = None

    def __new__(cls, path):
        if cls._instance is None:
            logger.info("Creating new SocialMedia connection...")
            cls._instance = super(SocialMedia, cls).__new__(cls)
            cls._instance.client = sqlite3.connect(path)
            cls._instance.create_table()
        return cls._instance
    
    def create_table(self):
        cursor = self.client.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                post_id INTEGER NOT NULL,
                text_content TEXT NOT NULL,
                date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.client.commit()
        cursor.close()
    
    def create_post(self, json_data):
        user_id, content = json_data['user_id'], json_data['text_content']
        cursor = self.client.cursor()
        cursor.execute(f"INSERT INTO posts (user_id, text_content) VALUES ({user_id}, '{content}')")
        self.client.commit()
        cursor.close()
    
    def get_all_posts(self):
        cursor = self.client.cursor()
        cursor.execute("SELECT text_content, date_time FROM posts")
        posts = cursor.fetchall()
        cursor.close()
        return posts


