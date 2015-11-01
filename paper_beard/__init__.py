"""
Main module of PaperBeard.
"""

import time

import os
from paper_beard import pdf_tools
from paper_beard.pdf_title import pdf_title
import random




google_scholar_result_fields = ["title", "author", "year", "citations", "link", "excerpt"]


for field in google_scholar_result_fields:
    csvOutputFile.write(field + "; ")
csvOutputFile.write("\n")

for root, directories, filenames in os.walk(args.inputFolder):
    for filename in filenames:
        # Get the full path to the file
        pathToFile = os.path.join(root, filename)

        # Check if this is actually a file
        if (not os.path.isfile(pathToFile)):
            continue

        # Check if this is a PDF file
        extension = os.path.splitext(pathToFile)[1]
        if (extension.lower() != '.pdf'):
            continue

        # Get the title of the paper from the metadata
        try:
            title = pdf_tools.getPDFTitle(pathToFile)
        except Exception as e:
            print("There was an error while getting the title of the PDF : " + pathToFile + ": " + str(e) + " The file will be skipped.")
            continue

        if (title == None or (str.strip(title) == "")):
            print("The metadata of the PDF-file " + pathToFile + " doesn't contain informations about the title. We will try the content of the PDF instead.")
            title = pdf_title(pathToFile)

        # Get the name of the author from the metadata
        author = pdf_tools.getPDFAuthor(pathToFile)

        googleScholarSearchString = title
        if (author != None):
            googleScholarSearchString += " " + author

        raw_scholar_data = Google(googleScholarSearchString, pages=1).search_scholar()

        if (len(raw_scholar_data["results"]) == 0):
            print("No Google Scholar result for file " + pathToFile + " with search string '" + googleScholarSearchString + "' found. This file will be skipped.")
            print("----")
            continue

        first_scholarresult = raw_scholar_data["results"][0];
        csv_scholarresult = ""

        for field in google_scholar_result_fields:
            if (field in first_scholarresult):
                csv_scholarresult += str(first_scholarresult[field])
            csv_scholarresult += "; "

        csv_scholarresult += "\n"

        csvOutputFile.write(csv_scholarresult)

        # Wait a moment to avoid getting tagged as a bot...
        time.sleep(0.5 + 3 * random.random())

csvOutputFile.close()
print("Getting Google Scholar results for PDF completed...")
