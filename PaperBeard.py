import os
import argparse
import random
from pyGoogleSearch import *
import time
from PDFTools import *
from pdftitle import pdf_title

__author__ = 'Malte Eckhoff'

# Parse arguments
parser = argparse.ArgumentParser(description='Parses PDFs from a folder and puts out a csv containing meta information (like ranking) for the contained PDFs.')
parser.add_argument('inputFolder', help='The folder from which the pdfs will be looked up on Google Scholar.')
parser.add_argument('outputCSVFile', help='The csv file where the extracted information about the PDF files will be written.')
args = parser.parse_args()

google_scholar_result_fields = ["title", "author", "year", "citations", "link", "excerpt"]

csvOutputFile = open(args.outputCSVFile, "w")

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
        title = PDFTools.getPDFTitle(pathToFile)

        if (title == None or (str.strip(title) == "")):
            print("The metadata of the PDF-file " + pathToFile + " doesn't contain informations about the title. We will try the content of the PDF instead.")
            title = pdf_title(pathToFile)

        # Get the name of the author from the metadata
        author = PDFTools.getPDFAuthor(pathToFile)

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
