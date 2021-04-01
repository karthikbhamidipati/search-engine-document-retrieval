import os

import pandas as pd

from utils.config import config


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
    dataset = pd.read_csv(input_path, sep=sep, names=headers, nrows=num_samples)
    if lookup_df and lookup_key:
        dataset = dataset[dataset[lookup_key].isin(lookup_df[lookup_key].to_list())]

    return dataset


def save_data(output_dir, file_name, df):
    """ TODO Add documentation, logging

    :param output_dir:
    :param file_name:
    :param df:
    :return:
    """
    output_path = os.path.join(output_dir, file_name)
    df.to_csv(output_path, index=False)


def subsample_docs(input_dir, output_dir=config.SUBSAMPLED_ROOT,
                   num_samples=config.NUM_SAMPLES):
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
    docs_sampled = read_data(input_dir, config.DOCS_FILE_NAME, '\t',
                             config.DOCS_HEADERS, num_samples=num_samples)

    save_data(output_dir, config.DOCS_FILE_NAME, docs_sampled)

    top100_sampled = read_data(input_dir, config.TOP100_FILE_NAME, r'\s+',
                               config.TOP100_HEADERS, lookup_df=docs_sampled,
                               lookup_key=config.DOCID_KEY)

    save_data(output_dir, config.TOP100_FILE_NAME, top100_sampled)

    queries_sampled = read_data(input_dir, config.QUERIES_FILE_NAME, '\t',
                                config.QUERIES_HEADERS, lookup_df=top100_sampled,
                                lookup_key=config.QUERYID_KEY)

    save_data(output_dir, config.QUERIES_FILE_NAME, queries_sampled)
