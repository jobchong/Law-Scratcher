from os import listdir
import string
import re 

casefolder = "/Users/wuguowei/Google Drive/Year 4 Sem 2/Artificial Intelligence/scrapelawnet/casesTXT/"
datafolder = "/Users/wuguowei/Google Drive/Year 4 Sem 2/Artificial Intelligence/scrapelawnet/data/"

#extracting level of court
#list of headers
headerlist = []                     
#counter
n=0
with open(datafolder+"data_court.txt", "w") as f:                              #opens a datafile
    for filename in listdir(casefolder):                                        #calling a txt file
        if filename.endswith(".txt") and not filename.startswith(".DS"):      
            with open(casefolder + filename) as currentCase:                    
                lines = currentCase.readlines()                                 #linify case
                
                courtdata = string.strip(string.strip(lines[4],"Tribunal/Court:" + "Tribunal/Court : "))        ###COURT RETRIEVE
                if courtdata == "High Court":
                    courtresult = "H"
                elif courtdata == "District Court": 
                    courtresult = "D"
                elif courtdata == "Magistrates Court":
                    courtrusult = "M"
                else:
                    courtresult = "NA"
               
                coramdata = lines[5].replace("Coram: ", "", 1)                                                  ### CORAM RETRIEVE
                coramdata = coramdata.replace(" Coram :  ", "", 1)
                
                
                
                ##continue to add the headers
                f.write(str(n)+","+courtresult+","+coramdata + "\n")
                print filename
                n += 1
                
                
    
