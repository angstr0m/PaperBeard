from typing import Optional

import click

import time
import paper_beard.export
import os
import paper_beard
import random


@click.group()
def cli():
    """CLI for a systematic literature review"""
    pass


@cli.group()
def manage():
    """Manages the lifecycle of a systematic literature review"""
    pass


@manage.command(name='create')
@click.argument('name')
def create_review(name: str):
    """Creates a new review process with the given NAME."""
    pass


@manage.command(name='view')
@click.option('--key', type=int, help='Display only review with given key')
def view_review(key: Optional[int]):
    """View one or all reviews"""
    pass


@cli.command()
@click.argument('input_folder', type=click.Path('r'))
@click.argument('output_csv_file', type=click.File('w+'))
def fetch(input_folder, output_csv_file):
    """Parses PDFs from INPUT_FOLDER and puts out OUTPUT_CSV_FILE containing
    meta information (like ranking) for the contained PDFs.
    """
    result = []
    for root, _, filenames in os.walk(input_folder):
        for filename in filenames:
            # Get the full path to the file
            path_to_file = os.path.join(root, filename)
            result.append(paper_beard.check(path_to_file))
            # Wait a moment to avoid getting tagged as a bot...
            time.sleep(0.5 + 3 * random.random())
    result = list(filter(None.__ne__, result))
    paper_beard.export.csv(result, output_csv_file)

    output_csv_file.close()


if __name__ == '__main__':
    cli()
