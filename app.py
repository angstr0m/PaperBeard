from typing import Optional

import click
from tabulate import tabulate

from paper_beard.models import Review, Protocol


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
    review = Review(name=name)
    protocol = Protocol()
    protocol.questions = 'EMPTY'
    review.protocol = protocol
    protocol.save()
    review.save()
    click.echo(review)


@manage.command(name='view')
@click.option('--key', type=int, help='Display only review with given key')
def view_review(key: Optional[int]):
    """View one or all reviews"""
    reviews = Review.select()
    click.echo(tabulate(map(lambda review: [review.id, review.name, review.created], reviews)))


if __name__ == '__main__':
    cli()
