from bs4 import BeautifulSoup
from os import listdir

# print """
# For fact paragraphs, type HN-Facts.
# For holding paragraphs, type HN-Held.
# For judgement paragraphs, type Judg-1.
# """

# searchTerm = raw_input("Which paragraphs do you want to search for? ")


searchTerm = ["misappropriated", "appeal", "dedication", "contribution", "compassion", "first-time", "deterrence", "public institution", "substantial", "premeditated", "fine"]

with open("/Users/jobchong/git/scrapelawnet/Output.txt", "w") as f:
    for filename in listdir("/Users/jobchong/git/scrapelawnet/"):
        if filename.endswith(".html"):
            with open("/Users/jobchong/git/scrapelawnet/" + filename) as currentCase:
                soup = BeautifulSoup(currentCase, "html.parser")
                facts = str(soup.find_all("p"))
                if searchTerm in currentCase:
                    f.write(facts)
