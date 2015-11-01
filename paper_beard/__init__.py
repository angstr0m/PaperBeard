"""
Main module of PaperBeard.
"""

import os
from paper_beard import pdf_tools
from paper_beard import pdf_title
from pyGoogleSearch import Google


def check(path_to_file):
    # Check if this is actually a file
    if not os.path.isfile(path_to_file):
        return

    # Check if this is a PDF file
    extension = os.path.splitext(path_to_file)[1]
    if extension.lower() != '.pdf':
        return

    # Get the title of the paper from the metadata
    try:
        title = pdf_tools.get_title(path_to_file)
    except Exception as e:
        print("There was an error while getting the title of the PDF : %s: %s The file will be skipped."
              % (path_to_file, str(e)))
        return

    if title is None or pdf_title.empty_str(title):
        print(
            "The metadata of the PDF-file %s doesn't contain information about the title."
            "We will try the content of the PDF instead." % path_to_file)
        title = pdf_title.title(path_to_file)

    # Get the name of the author from the metadata
    author = pdf_tools.get_author(path_to_file)

    search_string = title
    if author is not None:
        search_string += " " + author

    raw_scholar_data = Google(search_string, pages=1).search_scholar()

    if len(raw_scholar_data["results"]) == 0:
        print(
            "No Google Scholar result for file %s with search string '%s' found. This file will be skipped." %
            (path_to_file, search_string)
        )
        print("----")
        return

    print("Getting Google Scholar results for PDF completed...")
    return raw_scholar_data["results"][0]