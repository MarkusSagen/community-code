"""
A simple web scraper to collect data from the Knowledge Center's tutorials
"""
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Instantiate the BeautifulSoup object for the tutorials page
tutorials_url = "https://peltarion.com/knowledge-center/documentation/tutorials"
tutorials_html = urlopen(tutorials_url).read().decode("utf-8")
tutorials_soup = BeautifulSoup(tutorials_html, "lxml")

# Scrape the data and add question variations
data = []
for a in tutorials_soup.find_all("a", href=True):
    if (a.strong is not None):
        data.append([a.strong.getText(), "We have a tutorial called \"" + a.strong.getText()+ "\" here: " + a["href"]])
        data.append(["Can you tell me about " + a.strong.getText(), "We have a tutorial called \"" + a.strong.getText() + "\" here: " + a["href"]])
        data.append(["Can you help me with " + a.strong.getText(), "We have a tutorial called \"" + a.strong.getText() + "\" here: " + a["href"]])
        data.append(["I want to " + a.strong.getText(), "We have a tutorial called \"" + a.strong.getText() + "\" here: " + a["href"]])
        data.append(["How can I " + a.strong.getText(), "We have a tutorial called \"" + a.strong.getText() + "\" here: " + a["href"]])

# Write to a CSV file
with open("../datasets/TutorialsWithVariations.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    # Add the data
    writer.writerows(data)