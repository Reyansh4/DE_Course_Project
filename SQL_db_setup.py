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
        self.analytics_table()

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
                            INSERT IGNORE INTO stats (video_id, commentCount, viewCount, favoriteCount, dislikeCount, likeCount)
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

    def query_by_video_id(self, video_id):
        try:
            self.conn = mysql.connector.connect(**self.config)
            cursor = self.conn.cursor()

            cursor.execute('''
                SELECT * FROM stats WHERE video_id = %s
            ''', (video_id,))

            result = cursor.fetchall()

            return result

        except Exception as e:
            print(f"Error querying by video_id: {e}")
            return None

        finally:
            if self.conn:
                self.conn.close()

    def query_by_video_id_2(self, video_id):
        try:
            self.conn = mysql.connector.connect(**self.config)
            cursor = self.conn.cursor()

            cursor.execute('''
                SELECT * FROM engagement WHERE video_id = %s
            ''', (video_id,))

            result = cursor.fetchall()

            return result

        except Exception as e:
            print(f"Error querying by video_id: {e}")
            return None

        finally:
            if self.conn:
                self.conn.close()

    def performing_search(self, vid):
        vidstats_dict={}
        sql_result = self.query_by_video_id(vid)
        if sql_result:
            vidstats_dict = {
                'video_id': vid,
                'commentCount': sql_result[0][1],
                'viewCount': sql_result[0][2],
                'favoriteCount': sql_result[0][3],
                'dislikeCount': sql_result[0][4],
                'likeCount': sql_result[0][5]
            }
                
        return vidstats_dict
    
    def performing_search_2(self, vid):
        engmnts_dict={}
        sql_result = self.query_by_video_id_2(vid)
        if sql_result:
            engmnts_dict = {
                'video_id': vid,
                'engagement': sql_result[0][1],
                'engagement_ratio': sql_result[0][2],
                'clash_of_tastes': sql_result[0][3]
            }
                
        return engmnts_dict
    
    def analytics_table(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            cursor = self.conn.cursor()

            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS engagement (
                            video_id VARCHAR(255) PRIMARY KEY,
                            engagement INT,
                            engagement_ratio VARCHAR(10),
                            clash_of_tastes VARCHAR(10),
                            FOREIGN KEY (video_id) REFERENCES stats(video_id)
                           );
                           ''')
        
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            if self.conn:
                self.conn.close()

    def insert_engagement_details(self, folder_path='test'):
        try:
            self.conn = mysql.connector.connect(**self.config)
            cursor = self.conn.cursor()

            for filename in os.listdir(folder_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(folder_path, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        video_id = data['videoInfo']['id']
                        # No need to fetch statistics here, as you're using a SELECT statement below
                        cursor.execute('''
                            INSERT INTO engagement (video_id, engagement, engagement_ratio, clash_of_tastes)
                            SELECT
                                s.video_id,
                                (s.viewCount + s.likeCount + s.dislikeCount) AS engagement,
                                CASE WHEN s.likeCount >= s.viewCount / 10 THEN 'good' ELSE 'poor' END AS engagement_ratio,
                                CASE WHEN (s.likeCount - s.dislikeCount) >= 0 THEN 'Liking' ELSE 'disliking' END AS clash_of_tastes
                            FROM stats s
                            WHERE s.video_id = %s
                                       AND NOT EXISTS (
                                       SELECT 1 FROM engagement e where e.video_id = s.video_id
                                       )
                        ''', (video_id,))

                        self.conn.commit()

            print("Engagement Table created successfully!")
        except Exception as e:
            print(f"Error inserting engagement details: {e}")
        finally:
            if self.conn:
                self.conn.close()

if __name__ == "__main__":
    video_db =  VideoDatabase(user='root', password='Rey@nsh4', database='Course_Project')
    video_db.insert_videos()
    video_db.insert_engagement_details()