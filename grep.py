from bs4 import BeautifulSoup
from os import listdir
import string

# print """
# For fact paragraphs, type HN-Facts.
# For holding paragraphs, type HN-Held.
# For judgement paragraphs, type Judg-1.
# """

# searchTerm = raw_input("Which paragraphs do you want to search for? ")

#variables so we easier to make changes when working on different computers
outputtext = "/Users/wuguowei/Google Drive/Year 4 Sem 2/Artificial Intelligence/scrapelawnet/casesTXT/"
casefolder = "/Users/wuguowei/Google Drive/Year 4 Sem 2/Artificial Intelligence/scrapelawnet/140/"

#counter (for rough work)
n = 0 
# searchTerm = ["misappropriated", "appeal", "dedication", "contribution", "compassion", "first-time", "deterrence", "public institution", "substantial", "premeditated", "fine"]

#extracting main sentencing para
# searchTerm = ["months imprisonment"]
for filename in listdir(casefolder):
    with open(string.strip(outputtext+filename+" "+str(n),"html")+"txt", "w") as f:   #filenumber after filename because sort in extractor is a pain
        
        n += 1
        if filename.endswith(".html"):
            with open(casefolder + filename) as currentCase:
                soup = BeautifulSoup(currentCase, "html.parser")
                paras = soup.find_all("title")
                paras += soup.find_all("tr")  #to retrieve the headings and titles
                paras += soup.find_all("p")
                for para in paras:
                    parastrip = para.get_text()
                    f.write(parastrip.encode("utf-8")), f.write("\n")
#                     for i in searchTerm:
#                         if i in parastrip:
#                             f.write(str(n)), f.write(searchTerm) f.write("\n")
#                             f.write(filename) , f.write("\n")
#                             f.write(parastrip.encode("utf-8")), f.write("\n")
#                             #n += 1

                            
