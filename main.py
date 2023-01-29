from flask import Flask, render_template,request
import time
from query import Query
from model import Model
from indexer import Indexer


app = Flask(__name__)
indexer = Indexer('index.html')
ranking_model = Model(indexer.documents)
query_processor = Query(ranking_model)
        
@app.route('/')
def dictionary():
    return render_template('home.html')

@app.route("/query", methods=['POST'])
def upload():
    start = time.time()
    query = request.form['query']
    result = query_processor.search(query)
    end = time.time()
    times = end - start
    return render_template('dictionary.html', dictionary=result, num_docs=len(result), time=str(times) + " " + "seconds", search_query = query)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
