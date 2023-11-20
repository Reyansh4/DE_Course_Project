import os
import json
from pymongo import MongoClient

class VideoMongoDatabase:
    def __init__(self, database_url='mongodb://localhost:27017/', database_name='your_database'):
        self.client = MongoClient(database_url)
        self.db = self.client[database_name]
        self.create_collection()

    def create_collection(self):
        self.videos_collection = self.db['videos']

    def insert_videos(self, folder_path='test'):
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    self.videos_collection.insert_one(data)

        print("Videos inserted successfully!")

if __name__ == "__main__":
    video_mongo_db = VideoMongoDatabase(database_name='Course_Project')
    video_mongo_db.insert_videos()