from os import listdir
import string


casefolder = "/Users/wuguowei/Google Drive/Year 4 Sem 2/Artificial Intelligence/scrapelawnet/casesTXT/"
datafolder = "/Users/wuguowei/Google Drive/Year 4 Sem 2/Artificial Intelligence/scrapelawnet/data/"

#extracting level of court

n=0
with open(datafolder+"/data_court.txt", "w") as f:                              #opens a datafile
    for filename in listdir(casefolder):                                        #calling a txt file
        if filename.endswith(".txt"):       
            with open(casefolder + filename) as currentCase:                    
                lines = currentCase.readlines()
                courtdata = string.strip(string.lstrip(lines[4],"Tribunal/Court:" + "Tribunal/Court : "))
                if courtdata == "High Court":
                    result = "H"
                elif courtdata == "District Court": 
                    result = "D"
                else:
                    result = "NA"
                f.write(str(n)+","+result+"\n")
                n += 1
                
                
    
