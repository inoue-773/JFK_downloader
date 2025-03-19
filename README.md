# JFK Assassination Records PDF Downloader

A python script to automatically download JFK Assassination Records PDF files from national archives. 

## dependencies
```
pip install tqdm tkinter BeautifulSoup requests

```

## Links.py
Simple script to analyze a html file from natinal archives to extract pdf file links.
Saves links as a txt file.

## Downloader.py
Download pdf files in parallel. This script downloads 10 files maximum at the same time.
Upon running the script, you will be asked to specify where to save the pdf files. Just select your desired location and wait a little bit.
