from flask import Flask, render_template, request, jsonify
from SQL_db_setup import VideoDatabase
from Mongo_db_setup import VideoMongoDatabase

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('DE_frontend.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['searchQuery']

    mongo_db = VideoMongoDatabase(database_name='Course_Project')
    mongo_result = mongo_db.perform_search(search_query)

    sql_db = VideoDatabase(user='root', password='Rey@nsh4', database='Course_Project')
    sql_result = sql_db.performing_search(mongo_result)

    print("MongoDB Results:")
    for mongo_doc in mongo_result:
        print(mongo_doc)

    print("\nSQL Results:")
    for sql_doc in sql_result.values():
        print(sql_doc)

    return "Results printed in the console."

if __name__ == "__main__":
    app.run(debug=True)