from argparse import ArgumentParser

from app.search_engine import run
from service.index import index_docs
from service.subsample import subsample_docs


def is_sub_arg(arg):
    key, value = arg
    return value is not None and key != 'action'


def clean_args(args):
    action = args.action
    cleaned_args = dict(filter(is_sub_arg, args._get_kwargs()))
    return action, cleaned_args


def main():
    parser = ArgumentParser()
    action_parser = parser.add_subparsers(title="actions", dest="action", required=True,
                                          help="select action to execute")

    # args for subsampling
    subsample_parser = action_parser.add_parser("subsample", help="subsample docs")
    subsample_parser.add_argument("-r", "--original-root-dir", dest="root_dir", required=True,
                                  help="root directory of the original docs to be subsampled")
    subsample_parser.add_argument("-o", "--output-dir", dest="output_dir", required=False,
                                  help="output directory for the subsampled docs")
    subsample_parser.add_argument("-n", "--num-samples", dest="num_samples", required=False, type=int,
                                  help="number of records to be subsampled")

    # args for indexing
    index_parser = action_parser.add_parser("index", help="index docs to elasticsearch")
    index_parser.add_argument("-p", "--docs-path", dest="docs_path", required=False,
                              help="path to index docs to elasticsearch")

    # args for evaluation
    eval_parser = action_parser.add_parser("eval", help="evaluate queries from elasticsearch")
    eval_parser.add_argument("-p", "--queries-path", dest="queries_path", required=False,
                              help="evaluate queries from elasticsearch")

    # args for starting search engine application
    app_parser = action_parser.add_parser("start_app", help="start search engine application")
    app_parser.add_argument("-s", "-secret-key", dest="secret_key", required=False,
                            help="secret key to start the search engine application")
    app_parser.add_argument("-p", "--app-port", dest="port", required=False,
                            help="port to start the search engine application")

    action, args = clean_args(parser.parse_args())
    print(action, args)

    if action == 'subsample':
        subsample_docs(**args)
    elif action == 'index':
        index_docs(**args)
    elif action == 'start_app':
        run(**args)


if __name__ == '__main__':
    main()
