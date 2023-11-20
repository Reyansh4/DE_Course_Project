import mysql.connector
import os
import json

class VideoDatabase:
    def __init__(self, host='localhost', user='your_username', password='your_password', database='your_database'):
        self.conn = None
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
        }
        self.create_table()

    def create_table(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            cursor = self.conn.cursor()

            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS stats(
                           video_id VARCHAR(255) PRIMARY KEY,
                           commentCount INT,
                           viewCount INT,
                           favoriteCount INT,
                           dislikeCount INT,
                           likeCount INT
                           );
                           ''')
        
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            if self.conn:
                self.conn.close()

    def insert_videos(self, folder_path = 'test'):
        try:
            self.conn = mysql.connector.connect(**self.config)
            cursor = self.conn.cursor()

            for filename in os.listdir(folder_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        video_id = data['videoInfo']['id']
                        statistics = data['videoInfo']['statistics']
                        
                        cursor.execute('''
                            INSERT INTO stats (video_id, commentCount, viewCount, favoriteCount, dislikeCount, likeCount)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        ''', (video_id, statistics.get('commentCount', 0), statistics.get('viewCount', 0),
                              statistics.get('favoriteCount', 0), statistics.get('dislikeCount', 0),
                              statistics.get('likeCount', 0)))

                        self.conn.commit()

            print("Videos inserted successfully!")
        except Exception as e:
            print(f"Error inserting videos: {e}")
        finally:
            if self.conn:
                self.conn.close()       

if __name__ == "__main__":
    video_db =  VideoDatabase(user='root', password='Rey@nsh4', database='Course_Project')

    video_db.insert_videos()