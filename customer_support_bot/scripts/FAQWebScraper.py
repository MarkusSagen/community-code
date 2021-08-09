"""
A simple web scraper to pull data from the Peltarion Knowledge Center FAQ
"""
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Instantiate a BeautifulSoup object for the FAQ
faq_url = "https://peltarion.com/knowledge-center/documentation/faq"
faq_html = urlopen(faq_url).read().decode("utf-8")
faq_soup = BeautifulSoup(faq_html, "lxml")

# Scrape the text
paragraphs = faq_soup.find_all("div", {"class": "sect2"})
headings = []
texts = []
data = []
for p in paragraphs:
    headings.append(p.h3.text)
    texts.append(p.p.text)
    data.append([p.h3.text, p.p.text])

# Write to a CSV file
with open("../datasets/FAQ.csv", "w", newline="") as file:
    writer = csv.writer(file)
    # Add header row
    writer.writerow(["Question", "Answer"])
    # Add the data
    writer.writerows(data)