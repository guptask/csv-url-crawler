# CSV-URL-Crawler

This script parses a CSV that contains structured data, finds the URLs
and downloads these into the 'results' directory. Any error found is
recorded in 'errlog.txt'.
- chmod +x parse\_crawl.py (allow the script to be executable)
- ./parse\_crawl.py \<CSV file> (run the script)

### Packages Required
- python (code tested for < v3)
- python-pandas (can install using  pip install --user pandas)
