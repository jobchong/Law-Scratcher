import re
import os.path
import string
from bs4 import BeautifulSoup

topdir = "."
exten = ".html"
def step (ext, dirname, names):
    ext = ext.lower()

    for name in names:
        if name.lower().endswith(ext):
            currentCase = open(os.path.join(dirname, name)).read()
            soup = BeautifulSoup(currentCase, "html.parser")
            facts = soup.find_all("p", "HN-Facts")
            print facts

            
os.path.walk(topdir, step, exten)
