import re
import os.path
import string
from bs4 import BeautifulSoup

topdir = "."
exten = ".html"

print """
For fact paragraphs, type HN-Facts.
For holding paragraphs, type HN-Held.
For judgement paragraphs, type Judg-1.
"""

searchTerm = raw_input("Which paragraphs do you want to search for? ")


def step (ext, dirname, names):
    ext = ext.lower()

    for name in names:
        if name.lower().endswith(ext):
            with open(os.path.join(dirname, name)) as currentCase:
                soup = BeautifulSoup(currentCase, "html.parser")
                facts = soup.find_all("p", class_ = searchTerm)
                f = open("Output.txt", "w")
                f.write(str(facts))
                
os.path.walk(topdir, step, exten)
