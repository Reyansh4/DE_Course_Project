# **OBJECTIVE**
Develop a Video Search Engine Application with a comprehensive GUI.

# **KEY FEATURES**
Integrated use of MongoDB, Neo4j, and MySQL databases for a comprehensive video 
search engine. Utilizing MongoDB for efficient video file indexing, Neo4j for managing 
video relationships, and MySQL for storing relational information, including crucial click through data. 

# **TECH STACK**
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Neo4J](https://img.shields.io/badge/Neo4j-008CC1?style=for-the-badge&logo=neo4j&logoColor=white)</br>
[![dependency - Kivy](https://img.shields.io/badge/dependency-Kivy-green)](https://pypi.org/project/Kivy)
[![dependency - mysql-connector-python](https://img.shields.io/badge/dependency-mysql--connector--python-green)](https://pypi.org/project/mysql-connector-python)
[![dependency - neo4j](https://img.shields.io/badge/dependency-neo4j-green)](https://pypi.org/project/neo4j)
[![dependency - pymongo](https://img.shields.io/badge/dependency-pymongo-green)](https://pypi.org/project/pymongo)

# **WORKING**</br>
## **USAGE**
The way to use the app is clearly described in the [Presentation](Presentation.pdf).</br>
or watch the [tutorial](https://youtu.be/QAbIaa7mXuc) regarding the working of the app that i uploaded on youtube.

## **SETTING UP THE DB'S**
* The SQL is setup by using the MySQL-connector-python and initially we create two tables named as STATS and ENGAGEMENT and query in the above tables. Thw stats part in the .json files is stored in the SQLDB.</br>
* The MongoDB is used for the querying the keyword and return the best matching document videoID. Initially the data in MongoDB is added by the PyMongo Library. The complete document is stored in the DB excluding the stats part in the .json file.</br>
* The Neo4j is used to get the related videos to the searched videoID. Our DB has a node for every videoID. The node has attributes like videoID,Title,Tags,channelType as the node properties. so we used the **TAG CLUSTERING** to get the related videos. Every node is related to another node if they have same tags and the relation that is formed is [:RELATED]. this later helps us in getting the recommended videos. with a single videoId we get the other related videoID's.

## **BACKEND LOGIC**
Our logic behind the working was Initially we search the Keyword that is typed in the Search Query. That Keyword is searched in the MongoDB for the first best result. The queried VideoID is returned. The VideoId's is then used and queried in the Neo4j DB for the Related videos and this will return the videoID's we then query the details of the returned videoID's. The MongoDB returns the other data related to the specific videoID and the MySQL database returnd the statistics in stored for the particular videoID.

## **DATASET**
The Dataset is available [here](dataset.tar.gz). Extract the .tar .gz file and retrive the .json files. There are 500 .json file zipped in the tar file. Both the [tar](datset.tar.gz) and [dataset](test) are available in the Repository for the easy demonstration purpose. The format in which the .json files contains the data is represented below.



**HAPPY CODING!!!....**
