from flask import Flask, render_template, request

from utils.config import config
from utils.es_wrapper import ElasticWrapper

app = Flask(__name__)
es_wrapper = ElasticWrapper()


@app.route('/')
def home():
    return render_template('search.html')


def get_query(search_term):
    return {
        "query": {
            "multi_match": {
                "query": search_term,
                "fields": [
                    "title",
                    "body"
                ]
            }
        }
    }


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]

    vsm_res = es_wrapper.search_index(config.VSM_INDEX_KEY, get_query(search_term))
    bm25_res = es_wrapper.search_index(config.BM25_INDEX_KEY, get_query(search_term))

    return render_template('results.html', vsm=vsm_res, bm25=bm25_res)


def run(secret_key=config.APP_SECRET_KEY, port=config.APP_PORT):
    app.secret_key = secret_key
    app.run(host=config.LOCAL_HOST, port=port)
