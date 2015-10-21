__author__ = 'Malte Eckhoff'

from PyPDF2 import PdfFileReader

class PDFTools:
    def getPDFContent(path):
        content = ""
        # Load PDF into pyPDF
        pdf = PdfFileReader(open(path, "rb"))
        # Iterate pages
        for i in range(0, pdf.getNumPages()):
            # Extract text from page and add to content
            content += pdf.getPage(i).extractText() + "\n"
        # Collapse whitespace
        content = " ".join(content.replace(u"\xa0", " ").strip().split())
        return content

    def getPDFTitle(path):
        pdf = PdfFileReader(open(path, "rb"))
        metadata = pdf.getDocumentInfo()

        if (metadata is not None):
            if (metadata.title is not None):
                return str.strip(metadata.title)
        return ""

    def getPDFAuthor(path):
        pdf = PdfFileReader(open(path, "rb"))
        metadata = pdf.getDocumentInfo()

        if (metadata != None):
            return metadata.author