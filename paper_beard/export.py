"""
Export module for PaperBeard.

Every export function should have the following signature:

```
xyz_export(data: list[Result], buffer: StringIO) -> StringIO
```
"""
import csv
from collections import OrderedDict
from io import StringIO
from pybtex.database import BibliographyData, Entry


exportable_fields = ["title", "author", "year", "citations", "link", "excerpt"]


def csv_export(data, buffer) -> StringIO:
    """Formats the data into a csv stream and returns the value.

    Uses the exportable_fields list for querying the results and generating the header.

    :type buffer: StringIO
    :type data: list[Result]
    :param data: a list of result objects fetch from a search engine
    :param buffer: the stream in which the formatted data should be written
    :return a stream of data formatted as valid csv
    """
    writer = csv.DictWriter(
        buffer,
        delimiter=';',
        quotechar='|',
        quoting=csv.QUOTE_MINIMAL,
        fieldnames=OrderedDict(map(lambda x: tuple([x, None]), exportable_fields)),
        extrasaction='ignore'
    )
    writer.writeheader()
    writer.writerows(data)
    return buffer


def bibtex_export(data, buffer) -> StringIO:
    """Formats the data into a bibtex stream and returns the value.

    :type buffer: StringIO
    :type data: list[Result]
    :param data: a list of result objects fetch from a search engine
    :param buffer: the stream in which the formatted data should be written
    :return a stream of data formatted as valid bibtex
    """
    def create_entry(entry):
        bib_entry = Entry(entry.type, [
            ('author', entry.author),
            ('title', entry.title),
            ('journal', entry.journal),
            ('year', entry.year)])

        return bib_entry

    bibliography = BibliographyData(
        entries=[[e.key, create_entry(e)] for e in data]
    )
    return buffer.write(bibliography.to_string("bibtex"))
