import os

from dask import dataframe as dd

from utils.config import Config


def read_data(input_dir, file_name, sep, headers,
              num_samples=None, lookup_df=None,
              lookup_key=None):
    """ TODO Add logging, documentation

    :param input_dir:
    :param file_name:
    :param sep:
    :param headers:
    :param num_samples:
    :param lookup_df:
    :param lookup_key:
    :return:
    """

    input_path = os.path.join(input_dir, file_name)
    print('Subsampling {}'.format(input_path))
    dataset = dd.read_csv(input_path, sep=sep, names=headers)

    if num_samples:
        dataset = dataset.loc[:num_samples]
    elif lookup_df is not None and lookup_key:
        lookup_values = lookup_df[lookup_key].unique().compute()
        dataset = dataset[dataset[lookup_key].isin(lookup_values)]

    return dataset


def save_data(output_dir, file_name, df):
    """ TODO Add documentation, logging

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


def subsample_docs(input_dir, output_dir=Config.SUBSAMPLED_ROOT,
                   num_samples=Config.NUM_SAMPLES):
    """ TODO add documentation
        Input files should be stored in the below format:
            input_dir/
                |-> msmarco-docs.tsv
                |-> msmarco-doctrain-queries.tsv
                |-> msmarco-doctrain-top100

    :param num_samples:
    :param input_dir:
    :param output_dir:
    :return:
    """
    queries_sampled = read_data(input_dir, Config.QUERIES_FILE_NAME, '\t',
                                Config.QUERIES_HEADERS, num_samples=num_samples)

    save_data(output_dir, Config.QUERIES_FILE_SAMPLED, queries_sampled)

    top100_sampled = read_data(input_dir, Config.TOP100_FILE_NAME, r'\s+',
                               Config.TOP100_HEADERS, lookup_df=queries_sampled,
                               lookup_key=Config.QUERYID_KEY)

    # Fetching the top n docs for each query based on rank
    top100_sampled = top100_sampled.groupby(Config.QUERYID_KEY)
    top100_sampled = top100_sampled.apply(get_nsmallest).reset_index(drop=True)

    save_data(output_dir, Config.TOP100_FILE_SAMPLED, top100_sampled)

    docs_sampled = read_data(input_dir, Config.DOCS_FILE_NAME, '\t',
                             Config.DOCS_HEADERS, lookup_df=top100_sampled,
                             lookup_key=Config.DOCID_KEY)

    save_data(output_dir, Config.DOCS_FILE_SAMPLED, docs_sampled)
