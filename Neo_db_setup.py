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
        try:
            self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
            print("Connection Established successfully")
        except Exception as e:
            print(f"Error establishing connection: {e}")

    def get_most_connected_videos(self, video_id):
        self.connect()
        if self._driver is None:
            print("Error: Connection not established.")
            return []

        with self._driver.session() as session:
            query = (
                f"MATCH (v1:V {{id: '{video_id}'}})-[:SHARED_TAG]-(v2:V) "
                "WITH v2.id AS videoId, COUNT(*) AS connectionCount "
                "ORDER BY connectionCount DESC "
                "LIMIT 2 "
                "RETURN videoId"
            )
            result = session.run(query)
            connected_videos = [record["videoId"] for record in result]
            return connected_videos

if __name__ == "__main__":
    neo4j_importer = VideoGraphDatabase(uri="bolt://localhost:7687", user="neo4j", password="Rey@nsh4")
    neo4j_importer.connect()