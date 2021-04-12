import os

from dask import dataframe as dd

from utils.config import Config


def filter_rows(dataset, lookup_key, lookup_df):
    lookup_values = lookup_df[lookup_key].unique().compute()
    return dataset[dataset[lookup_key].isin(lookup_values)].reset_index(drop=True)


def read_data(input_dir, file_name, sep, headers=None):
    """
    :param input_dir:
    :param file_name:
    :param sep:
    :param headers:
    :return:
    """

    input_path = os.path.join(input_dir, file_name)
    print('Subsampling {}'.format(input_path))
    return dd.read_csv(input_path, sep=sep, names=headers)


def save_data(output_dir, file_name, df):
    """
    :param output_dir:
    :param file_name:
    :param df:
    :return:
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, file_name)
    print('Saving subsampled file {}'.format(output_path))
    df.to_csv(output_path, index=False, single_file=True)


def get_nsmallest(row):
    return row.nsmallest(Config.NUM_DOCS_PER_QUERY, 'rank')


def exists(input_dir, file_name):
    return os.path.exists(os.path.join(input_dir, file_name))


def subsample_docs(input_dir, output_dir=Config.SUBSAMPLED_ROOT,
                   num_samples=Config.NUM_SAMPLES):
    """
        Input files should be stored in the below format:
            input_dir/
                |-> msmarco-docs.tsv
                |-> msmarco-doctrain-queries.tsv
                |-> msmarco-doctrain-top100
                |-> msmarco-clustered-queries.csv (Optional)

    :param num_samples:
    :param input_dir:
    :param output_dir:
    :return:
    """
    # reading queries
    if Config.USE_CLUSTERS and exists(input_dir, Config.CLUSTERED_QUERIES_FILE_NAME):
        queries_sampled = read_data(input_dir, Config.CLUSTERED_QUERIES_FILE_NAME, ',')
        queries_sampled = queries_sampled[queries_sampled.cluster.isin(Config.CLUSTER_IDS)].reset_index(drop=True)
        queries_sampled = queries_sampled.drop('cluster', axis=1)
    else:
        queries_sampled = read_data(input_dir, Config.QUERIES_FILE_NAME, '\t',
                                    Config.QUERIES_HEADERS)

    # sampling top 100 dataset
    top100_sampled = read_data(input_dir, Config.TOP100_FILE_NAME, r'\s+',
                               Config.TOP100_HEADERS)

    # removing queries with no ranking
    queries_sampled = filter_rows(queries_sampled, Config.QUERYID_KEY, top100_sampled)

    # sampling queries
    queries_sampled = queries_sampled.loc[: num_samples - 1].reset_index(drop=True)
    top100_sampled = filter_rows(top100_sampled, Config.QUERYID_KEY, queries_sampled)

    # Fetching the top n docs for each query based on rank
    top100_sampled = top100_sampled.groupby(Config.QUERYID_KEY)
    top100_sampled = top100_sampled.apply(get_nsmallest).reset_index(drop=True)

    # sampling docs using ids from top100
    docs_sampled = read_data(input_dir, Config.DOCS_FILE_NAME, '\t',
                             Config.DOCS_HEADERS)
    docs_sampled = filter_rows(docs_sampled, Config.DOCID_KEY, top100_sampled)

    save_data(output_dir, Config.QUERIES_FILE_SAMPLED, queries_sampled)
    save_data(output_dir, Config.TOP100_FILE_SAMPLED, top100_sampled)
    save_data(output_dir, Config.DOCS_FILE_SAMPLED, docs_sampled)
