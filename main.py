from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    action_parser = parser.add_subparsers(title="actions", dest="action", required=True,
                                          help="select action to execute")

    # args for subsampling
    subsample_parser = action_parser.add_parser("subsample", help="subsample docs")
    subsample_parser.add_argument("-sr", "--original-root-dir", dest="original_root_dir", required=True,
                                  help="root directory of the original docs to be subsampled")
    subsample_parser.add_argument("-so", "--output-dir", dest="subsampled_dir", required=False,
                                  help="output directory for the subsampled docs")
    subsample_parser.add_argument("-sn", "--num-samples", dest="num_samples", required=False, type=int,
                                  help="number of records to be subsampled")

    # args for indexing
    index_parser = action_parser.add_parser("index", help="index docs to elasticsearch")
    index_parser.add_argument("-id", "--docs-path", dest="index_docs_path", required=False,
                              help="path to index docs to elasticsearch")

    # args for starting search engine application
    app_parser = action_parser.add_parser("start_app", help="start search engine application")
    app_parser.add_argument("-as", "-secret-key", dest="secret_key", required=False,
                            help="secret key to start the search engine application")
    app_parser.add_argument("-ap", "--app-port", dest="app_port", required=False,
                            help="port to start the search engine application")

    args = parser.parse_args()
    print(args)


if __name__ == '__main__':
    main()
