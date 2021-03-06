#!/usr/bin/env python2

"""Parse a CSV, find URLs and download these in a certain format"""

__author__ = "Sounak Gupta"
__license__ = "GPLv3"

import sys, re, os, requests, mimetypes, glob
import pandas as pd

if len(sys.argv) != 2 :
    raise ValueError("Enter ./parse_crawl <csv_file>")

logfile = "errlog.txt"
if os.path.exists(logfile):
    os.remove(logfile)

df = pd.read_csv(filepath_or_buffer = sys.argv[1])

for i,row in df.iterrows():
    unique_id = str(row["Name"]) + r' - ' + str(row["Email"])
    path = r'results/' + unique_id + r'/'
    file_tag = path + unique_id + r' - '
    print(unique_id)
    j = 0

    for x in row:
        val = str(x)
        j += 1

        # Parse for URLs
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', val)
        if not urls:
            continue
        if len(urls) > 1:
            raise AssertionError()
        if not os.path.exists(path):
            os.makedirs(path)

        # Form the filename
        col_name = str(df.columns[j-1])
        file_name = file_tag + col_name

        # Search for existing files with matching name
        found = glob.glob(file_name + "*")
        if len(found) > 1:
            raise AssertionError()
        if len(found) == 1:
            print("\t[old] " + col_name)
            continue

        # Extract file extension from HTTP header
        extension = ""
        response = requests.get(urls[0], allow_redirects=True)
        if r'Content-Type' not in response.headers.keys():
            print("\t[err] " + col_name)
            log_fd = open('errlog.txt','a')
            log_fd.write(unique_id + r' - ' + col_name + "\n")
            log_fd.close()
        else:
            print("\t[new] " + col_name)
            content_type = response.headers['Content-Type']
            extension = mimetypes.guess_extension(content_type)

        file_fd = open(file_name + extension, 'wb')
        file_fd.write(response.content)
        file_fd.close()

