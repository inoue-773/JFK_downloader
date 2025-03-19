#!/usr/bin/env python3
import sys
import csv
import requests
from bs4 import BeautifulSoup

def extract_pdf_urls_from_url(url):
    # Download the page content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve URL: {url} (status code: {response.status_code})")
        sys.exit(1)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    
    pdf_urls = set()
    # Find all <a> tags with an href attribute that ends with .pdf
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.lower().endswith('.pdf'):
            pdf_urls.add(href)
    
    # Prepend the base URL if the link is relative
    base_url = "https://www.archives.gov"
    full_urls = []
    for link in pdf_urls:
        if not link.startswith("http"):
            full_url = base_url + link
        else:
            full_url = link
        full_urls.append(full_url)
    
    return sorted(full_urls)

def write_txt(urls, output_txt):
    with open(output_txt, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for url in urls:
            writer.writerow([url])

def main():
    url = "https://www.archives.gov/research/jfk/release-2025"
    output_txt = "jfk_pdfs.txt"
    
    pdf_urls = extract_pdf_urls_from_url(url)
    write_txt(pdf_urls, output_txt)
    
    print(f"Extracted {len(pdf_urls)} PDF URLs from {url} and saved them to {output_txt}")

if __name__ == "__main__":
    main()
