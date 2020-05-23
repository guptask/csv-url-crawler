#!/usr/bin/env python

import sys, re, os, requests, mimetypes
import pandas as pd

def i2alpha(x):
    if not x:
        raise AssertionError()
    s = ''
    while x != 0:
        s = chr(97 + x%26 - 1) + s
        x /= 26
    return s

if len(sys.argv) != 2 :
    raise ValueError("Enter ./parse_crawl <csv_file>")

df = pd.read_csv(filepath_or_buffer = sys.argv[1])
for i,row in df.iterrows():
    path = "results/" + row["Name"] + "/"
    print(row["Name"]),
    j = 0
    for x in row:
        val = str(x)
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', val)
        j += 1
        if not urls:
            continue
        if len(urls) > 1:
            raise AssertionError()
        if not os.path.exists(path):
            os.makedirs(path)
        col_name = i2alpha(j)
        print(col_name),
        response = requests.get(urls[0], allow_redirects=True)
        content_type = response.headers['content-type']
        extension = mimetypes.guess_extension(content_type)
        open(path + col_name + extension, 'wb').write(response.content)
    print("")
