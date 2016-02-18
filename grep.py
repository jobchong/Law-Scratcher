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
            currentCase = open(os.path.join(dirname, name)).read()
            soup = BeautifulSoup(currentCase, "html.parser")
            facts = soup.find_all("p", class_ = searchTerm)
            file = open("Output.txt", "w")
            file.write(unicode(facts))
            file.close()

            
os.path.walk(topdir, step, exten)
