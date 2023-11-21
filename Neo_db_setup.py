import os
import json
from py2neo import Graph

class VideoGraphDatabase:
    def __init__(self, uri, user, password):
        self.graph = Graph(uri, auth=(user, password))

    def insert_videos(self, folder_path='test'):
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    video_id = data['videoInfo']['id']
                    tags = data['videoInfo']['snippet']['tags']

                    query_create_node = f"CREATE (:Video {{videoId: '{video_id}'}})"
                    self.graph.run(query_create_node)

                    for tag in tags:
                        query_add_attribute = f"MATCH (v:Video {{videoId: '{video_id}'}}) SET v.{tag} = true"
                        self.graph.run(query_add_attribute)
        
        print("Inserted the videos successfully")

if __name__ == "__main__":
    neo4j_importer = VideoGraphDatabase(uri="bolt://localhost:7687", user="neo4j", password="Rey@nsh4")
    neo4j_importer.insert_videos()