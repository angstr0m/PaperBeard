"""

"""


google_scholar_fields = ["title", "author", "year", "citations", "link", "excerpt"]


def csv(data, file_handle):
    for field in google_scholar_fields:
        file_handle.write(field + "; ")
    file_handle.write("\n")
    csv_scholar_result = ""

    for row in data:
        for field in google_scholar_fields:
            if field in row:
                csv_scholar_result += str(row[field])
            csv_scholar_result += "; "
        csv_scholar_result += "\n"

    file_handle.write(csv_scholar_result)
    file_handle.close()
