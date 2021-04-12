from flask import Flask, render_template, request

from utils.config import config
from utils.es_wrapper import ElasticWrapper

app = Flask(__name__.split('.')[-1], template_folder="web/templates", static_folder="web/static")
es_wrapper = ElasticWrapper()


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


def get_suggestions(search_term):
    return {
            "query": {
                "match": {
                    "query": search_term
                }
            },
            "fields": ["title"],
            "_source": False
    }


@app.route('/')
def home():
    return render_template('search.html')


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():
    search_term = request.form["input"]

    vsm_res = es_wrapper.search_index(config.VSM_INDEX_KEY, get_query(search_term))
    bm25_res = es_wrapper.search_index(config.BM25_INDEX_KEY, get_query(search_term))

    return render_template('results.html', vsm=vsm_res, bm25=bm25_res, search_term=search_term)


@app.route('/suggestions')
def suggestions():
    search_term = request.args.get('search_query')
    print("Search term{}".format(search_term))
    query_suggestions = es_wrapper.search_index(config.BM25_INDEX_KEY, get_suggestions(search_term))
    return render_template('suggestions.html', suggestions=query_suggestions)


def run(secret_key=config.APP_SECRET_KEY, port=config.APP_PORT):
    app.secret_key = secret_key
    app.run(host=config.LOCAL_HOST, port=port)
