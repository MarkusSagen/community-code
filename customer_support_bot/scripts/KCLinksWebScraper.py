"""
A simple webscraper to pull content from the Knowledge Center's links
"""
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Instantiate a BeautifulSoup object for the links 
links_url = "https://peltarion.com/knowledge-center/documentation"
links_html = urlopen(links_url).read().decode("utf-8")
links_soup = BeautifulSoup(links_html, "lxml")

# Create varations of user questions and answers with links
data = []
for a in links_soup.find_all("a", href=True):
    data.append([a.text, "You can read about " + a.text + " here: " + a["href"]])
    data.append(["I want to know how to " + a.text, "You can read about " + a.text + " here: " + a["href"]])
    data.append(["I want to know more about " + a.text, "You can read about " + a.text + " here: " + a["href"]])
    data.append(["What is " + a.text + "?", "You can read about " + a.text + " here: " + a["href"]])
    data.append(["What does " + a.text + " mean?", "You can read about " + a.text + " here: " + a["href"]])

# Write to a CSV file
with open("../datasets/LinksWithVariations.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    # Add the data
    writer.writerows(data)