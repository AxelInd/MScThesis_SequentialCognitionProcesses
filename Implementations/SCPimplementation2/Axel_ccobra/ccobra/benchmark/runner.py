""" Imports a given python script and instantiates the contained model if
available.

Copyright 2018 Cognitive Computation Lab
University of Freiburg
Nicolas Riesterer <riestern@tf.uni-freiburg.de>
Daniel Brand <daniel.brand@cognition.uni-freiburg.de>

"""

import argparse
import os
import sys
from contextlib import contextmanager

import pandas as pd

from . import evaluator
from . import server
from . import comparator
from . import benchmark as bmark
from .visualization import html_creator, viz_plot

def parse_arguments():
    """ Parses the command line arguments for the benchmark runner.

    Returns
    -------
    dict
        Dictionary mapping from cmd arguments to values.

    """

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('benchmark', type=str, help='Benchmark file.')
    parser.add_argument('-m', '--model', type=str, help='Model file.')
    parser.add_argument(
        '-o', '--output', type=str, default='browser', help='Output style (browser/html).')
    parser.add_argument('-c', '--cache', type=str, help='Load specified cache file.')
    parser.add_argument('-s', '--save', type=str, help='Store results as csv table.')
    parser.add_argument(
        '-cn', '--classname', type=str,
        help='Load a specific class from a folder containing multiple classes.')

    args = vars(parser.parse_args())

    if not args['model'] and not args['benchmark']:
        print('ERROR: Must specify either model or benchmark.')
        parser.print_help()
        sys.exit(99)

    return args

@contextmanager
def silence_stdout(silent, target=os.devnull):
    """ Contextmanager to silence stdout printing.

    Parameters
    ----------
    silent : bool
        Flag to indicate whether contextmanager should actually silence stdout.

    target : filepath, optional
        Target to redirect silenced stdout output to. Default is os.devnull.
        Can be modified to point to a log file instead.

    """

    new_target = open(target, 'w') if silent else sys.stdout
    old_target, sys.stdout = sys.stdout, new_target
    try:
        yield new_target
    finally:
        sys.stdout = old_target

def main(args):
    """ Main benchmark routine. Parses the arguments, loads models and data,
    runs the evaluation loop and produces the output.

    Parameters
    ----------
    args : dict
        Command line argument dictionary.

    """

    # Compose the model list
    modellist = []
    if args['model']:
        modellist.append(bmark.ModelInfo(args['model'], os.getcwd(), args['classname']))

    # Load the benchmark settings
    benchmark = None
    benchmark = bmark.load_benchmark(args['benchmark'])
    corresponding_data = False
    if 'corresponding_data' in benchmark:
        corresponding_data = benchmark['corresponding_data']

    # Only extend if not cached
    cache_df = None
    if not args['cache']:
        modellist.extend(benchmark['models'])
    else:
        cache_df = pd.read_csv(args['cache'])

    # Extract comparator settings from benchmark description
    eval_comparator = comparator.EqualityComparator()
    if 'comparator' in benchmark:
        if benchmark['comparator'] == 'nvc':
            eval_comparator = comparator.NVCComparator()

    # Run the model evaluation
    is_silent = (args['output'] in ['html', 'server'])
    eva = None
    if benchmark['type'] == 'adaption':
        eva = evaluator.AdaptionEvaluator(
            modellist,
            eval_comparator,
            benchmark['data.test'],
            train_datafile=benchmark['data.train'],
            train_data_person=benchmark['data.train_person'],
            silent=is_silent,
            corresponding_data=corresponding_data,
            domain_encoders=benchmark['domain_encoders'],
            cache_df=cache_df
        )
    elif benchmark['type'] == 'coverage':
        # Check for benchmark validity
        if benchmark['data.train'] or benchmark['data.train_person']:
            print('WARNING: Ignoring specified training and train_person data ' \
                  + 'for coverage evaluation...')

        eva = evaluator.CoverageEvaluator(
            modellist,
            eval_comparator,
            benchmark['data.test'],
            train_datafile=benchmark['data.train'],
            train_data_person=benchmark['data.train_person'],
            silent=is_silent,
            corresponding_data=corresponding_data,
            domain_encoders=benchmark['domain_encoders'],
            cache_df=cache_df
        )
    else:
        raise ValueError('Unknown benchmark type: {}'.format(benchmark['type']))

    with silence_stdout(is_silent):
        res_df = eva.evaluate()

    if 'save' in args:
        res_df.to_csv(args['save'], index=False)

    # Run the metric visualizer
    htmlcrtr = html_creator.HTMLCreator([
        viz_plot.AccuracyVisualizer(),
        viz_plot.BoxplotVisualizer(),
        viz_plot.TableVisualizer()
    ])

    # Prepare the benchmark output information and visualize the evaluation results
    benchmark_info = {
        'name': os.path.basename(args['benchmark']),
        'data.train': os.path.basename(
            benchmark['data.train']) if benchmark['data.train'] else '',
        'data.train_person': os.path.basename(
            benchmark['data.train_person']) if benchmark['data.train_person'] else '',
        'data.test': os.path.basename(benchmark['data.test']),
        'type': benchmark['type'],
        'corresponding_data': benchmark['corresponding_data'],
        'domains': list(res_df['domain'].unique()),
        'response_types': list(res_df['response_type'].unique()),
    }

    if args['output'] == 'browser':
        html = htmlcrtr.to_html(res_df, benchmark_info, embedded=False)
        server.load_in_default_browser(html.encode('utf8'))
    elif args['output'] == 'server':
        html = htmlcrtr.to_html(res_df, benchmark_info, embedded=True)
        sys.stdout.buffer.write(html.encode('utf-8'))
    elif args['output'] == 'html':
        html = htmlcrtr.to_html(res_df, benchmark_info, embedded=False)
        print(html)

def entry_point():
    """ Entry point for the CCOBRA executables.

    """

    args = parse_arguments()

    try:
        main(args)
    except Exception as exc:
        if args['output'] != 'html':
            raise
        msg = 'Error: ' + str(exc)
        if args['output'] == 'html':
            print('<p>{}</p><script>document.getElementById(\"result\").style.backgroundColor ' \
                '= \"Tomato\";</script>'.format(msg))
        else:
            print(exc)
        sys.exit()

if __name__ == '__main__':
    entry_point()
