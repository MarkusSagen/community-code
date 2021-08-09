"""
A quick web scraper to collect data from Peltarion's Glossary and Documentation menu in the
Knowledge Center.
"""
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Setting up Beautiful Soup for the Glossary and Menu
glossary_url = "https://peltarion.com/knowledge-center/documentation/glossary"
glossary_html = urlopen(glossary_url).read().decode("utf-8")
glossary_soup = BeautifulSoup(glossary_html, "lxml")

menu_url = "https://peltarion.com/knowledge-center/documentation"
menu_html = urlopen(menu_url).read().decode("utf-8")
menu_soup = BeautifulSoup(menu_html, "lxml")

menu_data = []
for a in menu_soup.find_all("a", href=True):
    if a.text != '':
        menu_data.append([a.text, "You can read about " + a.text + " here: " + a["href"]])

# Separate the Glossary's sections into lists of headers and lists of paragraphs
divs = glossary_soup.find_all("div", {"class": "sect2"})
headings = []
paragraphs = []
for p in divs:
    if p.find("div"):
        headings.append(p.h3.text)
        paragraphs.append(p.find_all("p"))

# Remove any HTML formatting and preserve just the text
textlist = []
for paragraph in paragraphs:
    text = ""
    for section in paragraph:
        text += section.text
    textlist.append(text)

# Scrape the Glossary, combine with relevant links, and generate variations of user questions
glossary_data = []
for i in range(len(headings)):
    linktext = ""
    for menu_item in menu_data:
        menu_title = menu_item[0]
        menu_link = menu_item[1]
        if (headings[i] != "") and ((headings[i] in menu_title) or (menu_title in headings[i])):
            linktext = " " + menu_link

    row = [headings[i], textlist[i] + linktext]
    glossary_data.append(row)
    row = ["What is " + headings[i], textlist[i] + linktext]
    glossary_data.append(row)
    row = ["Can you help me with " + headings[i], textlist[i] + linktext]
    glossary_data.append(row)
    row = ["What does " + headings[i] + " mean?", textlist[i] + linktext]
    glossary_data.append(row)
    row = ["How do I use " + headings[i] + "?", textlist[i] + linktext]
    glossary_data.append(row)

# Write to a CSV file
with open("../datasets/GlossaryWithVariations.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    # Add header row
    writer.writerow(["Question", "Answer"])
    # Add the data
    writer.writerows(glossary_data)