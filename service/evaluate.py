import os

import dask.dataframe as dd

from utils.config import Config
from utils.es_wrapper import ElasticWrapper


def get_queries(queries_path):
    top100_df = dd.read_csv(os.path.join(queries_path, Config.TOP100_FILE_SAMPLED))
    top100_df = top100_df[['docid', 'rank', 'qid']].groupby('qid').agg([list]).reset_index()
    top100_df.columns = top100_df.columns.droplevel(1)
    queries_df = dd.read_csv(os.path.join(queries_path, Config.QUERIES_FILE_SAMPLED))
    return queries_df.merge(top100_df, how='left', on='qid')


def get_doc_ratings(index, doc_ids, ranks):
    doc_ratings = []
    for doc_id, rank in zip(doc_ids, ranks):
        doc_ratings.append(
            {
                "_index": index,
                "_id": doc_id,
                "rating": rank
            }
        )
    return doc_ratings


def get_requests(index, queries_df):
    requests = []
    for _, query_row in queries_df.iterrows():
        requests.append(
            {
                "id": str(query_row['qid']),
                "request": {
                    "query": {
                        "multi_match": {
                            "query": query_row['query'],
                            "fields": [
                                "title",
                                "body"
                            ]
                        }
                    }
                },
                "ratings": get_doc_ratings(index, query_row['docid'], query_row['rank'])
            }
        )
    return requests


def rank_eval_query(index, es_wrapper, queries_df):
    request_body = {
        "requests": get_requests(index, queries_df),
        "metric": {
            "dcg": {
                "k": 10,
                "normalize": "true"
            }
        }
    }
    return es_wrapper.rank_eval(index, request_body)


def rank_eval(queries_path=Config.SUBSAMPLED_ROOT):
    es_wrapper = ElasticWrapper()
    queries_df = get_queries(queries_path)

    vsm_metrics = rank_eval_query(Config.VSM_INDEX_KEY, es_wrapper, queries_df)
    bm25_metrics = rank_eval_query(Config.BM25_INDEX_KEY, es_wrapper, queries_df)

    print(vsm_metrics, bm25_metrics)

    es_wrapper.close()
