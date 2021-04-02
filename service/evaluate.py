import os

import pandas as pd

from utils.config import Config
from utils.es_wrapper import ElasticWrapper


def get_doc_ratings(index, doc_ids, ranks):
    for doc_id, rank in enumerate(doc_ids, ranks):
        yield {
            "_index": index,
            "_id": doc_id,
            "rating": rank
        }


def get_requests(index, queries_df):
    for _, query_row in queries_df.iterrows():
        yield {
            "id": query_row.qid,
            "request": {
                "query": {
                    "multi_match": {
                        "query": query_row.query,
                        "fields": [
                            "url",
                            "title",
                            "body"
                        ]
                    }
                }
            },
            "ratings": get_doc_ratings(index, query_row.doc_ids, query_row.ranks)
        }


def rank_eval_query(index, es_wrapper, queries_df):
    request_body = {
        "requests": get_requests(index, queries_df),
        "metric": {
            "precision": {
                "k": 10,
                "relevant_rating_threshold": 1,
                "ignore_unlabeled": "false"
            }
        }
    }
    return es_wrapper.rank_eval(index, request_body)


def get_queries(queries_path):
    top100_df = pd.read_csv(os.path.join(queries_path, Config.TOP100_FILE_NAME))
    top100_df = top100_df[['docid', 'rank', 'qid']].groupby('qid').agg(lambda x: list(x))
    queries_df = pd.read_csv(os.path.join(queries_path, Config.QUERIES_FILE_NAME))
    return queries_df.merge(top100_df, how='left', on='qid')


def rank_eval(queries_path=Config.SUBSAMPLED_ROOT):
    es_wrapper = ElasticWrapper()
    queries_df = get_queries(queries_path)

    vsm_metrics = rank_eval_query(Config.VSM_INDEX_KEY, es_wrapper, queries_df)
    bm25_metrics = rank_eval_query(Config.BM25_INDEX_KEY, es_wrapper, queries_df)

    print(vsm_metrics, bm25_metrics)

    es_wrapper.close()
