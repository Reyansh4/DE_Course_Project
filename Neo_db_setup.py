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

if __name__ == "__main__":
    neo4j_importer = VideoGraphDatabase(uri="bolt://localhost:7687", user="neo4j", password="Rey@nsh4")
    neo4j_importer.connect()