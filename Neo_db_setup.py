import os
import json
from neo4j import GraphDatabase

class VideoGraphDatabase:
    def __init__(self, uri, user, password):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

    def insert_videos(self, folder_path='test'):
        with self._driver.session() as session:
            for filename in os.listdir(folder_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)

                        if 'videoInfo' in data and 'snippet' in data['videoInfo']:
                            video_id = data['videoInfo']['id']
                            
                            if 'tags' in data['videoInfo']['snippet']:
                                tags = [tag.replace(' ', '_') for tag in data['videoInfo']['snippet']['tags']]

                                query_create_node = f"""
                                    MERGE (v:Video {{videoId: '{video_id}'}})
                                    SET {', '.join([f'v.{tag} = true' for tag in tags])}
                                """
                                session.run(query_create_node)
                            else:
                                print(f"No 'tags' key in 'snippet' for file: {filename}")
                        else:
                            print(f"Expected keys 'videoInfo' or 'snippet' not found for file: {filename}")

        print("Inserted the videos successfully")

if __name__ == "__main__":
    neo4j_importer = VideoGraphDatabase(uri="bolt://localhost:7687", user="neo4j", password="Rey@nsh4")
    neo4j_importer.connect()
    neo4j_importer.insert_videos()