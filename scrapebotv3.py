#install the beautifulsoup library and the requests library before use!

#provide your user inputs:

username = raw_input("Username here: ")
password = raw_input("Password here: ")
searchTerm = raw_input("What do you want to search for? ")
specified_resources = [1,2] #1 = "Judgments", 2 = "Singapore Law Reports"

#doing imports for making requests and parsing
import requests #used to handle logins and cookies
from bs4 import BeautifulSoup #used to parse websites

#doing imports to slow down the bot
import random; import datetime; import time; random.seed(datetime.datetime.now())
def sleepabit():
    time.sleep(random.uniform(2,8))

# imports for saving files
import pickle #to save files
def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
        
#Handles the security certificate by lawnet. this part is to set the TLS certficate to v1.0. I found the solution at: http://stackoverflow.com/questions/14102416/python-requests-requests-exceptions-sslerror-errno-8-ssl-c504-eof-occurred
  
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1) #eclipse flags an error, but the import works

#defining functions that will be used to determine the URLs that lawnet will generate from our searches

def returnCombinedURL(searchId, currentPageNumber):
    combinedurl = ("https://www-lawnet-sg.lawproxy1.nus.edu.sg/lawnet/group/lawnet/result-page?p_p_id=legalresearchresultpage_WAR_lawnet3legalresearchportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_legalresearchresultpage_WAR_lawnet3legalresearchportlet_selectedSortFilter=relevance&_legalresearchresultpage_WAR_lawnet3legalresearchportlet_isParentFilterSelected=false&_legalresearchresultpage_WAR_lawnet3legalresearchportlet_isGrandParentFilterSelected=false&_legalresearchresultpage_WAR_lawnet3legalresearchportlet_action=actionPageNo&_legalresearchresultpage_WAR_lawnet3legalresearchportlet_searchId=" + \
                   str(searchId) + \
                   "&_legalresearchresultpage_WAR_lawnet3legalresearchportlet_enteredkeywordNumber=10&_legalresearchresultpage_WAR_lawnet3legalresearchportlet_cur=" + \
                   str(currentPageNumber) + \
                   "&_legalresearchresultpage_WAR_lawnet3legalresearchportlet_pre=0") 
    return combinedurl

def returnlistofURLsofResultPages(searchId, lastPageNumber):
    listofURLsofResultPages = []
    for i in range(1, lastPageNumber + 1):
        listofURLsofResultPages.append(returnCombinedURL(searchId, i))
    return listofURLsofResultPages

def returnListofDocumentURLsonResultspage(bsObj):
    
    listofDocumentUrlsonpage = []
    
    for htmltag in bsObj.findAll('a', {"class": "document-title"}):
        contentDocID = htmltag['onclick'].split("viewPageContent('")[1].replace("')","")
        contentDocID = contentDocID.replace(" ", "%20") #this yields contentDocID
        finalurlofdocument = "https://www-lawnet-sg.lawproxy1.nus.edu.sg/lawnet/group/lawnet/page-content?p_p_id=legalresearchpagecontent_WAR_lawnet3legalresearchportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_legalresearchpagecontent_WAR_lawnet3legalresearchportlet_action=openContentPage&contentDocID=" + \
                             contentDocID
        listofDocumentUrlsonpage.append(finalurlofdocument)

    return listofDocumentUrlsonpage

#starts a session with Lawnet

session = requests.Session()

session.mount("https://", MyAdapter()) #this is to make the session use the TLSv1 certificate

#HTTP headers that disguises bot as a human! IMPORTANT. This sends all 7 headers that a normal browser does
  
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Accept-Language": "en-GB,en-US;q=0.8,en;q=0.6",
           "Upgrade-Insecure-Requests": "1"} 

#THE BOT WILL NOW LOG IN TO THE NUS PROXY PAGE
   
params = {"domain": "NUSSTU", "user": username, "pass": password}  #target site has the login fields "user" and "pass"
loginformphpurl = "https://proxylogin.nus.edu.sg/lawproxy1/public/login_form.asp?logup=false&url=http://www.lawnet.sg/lawnet/ip-access"  #original program in book uses "url" rather than "loginurl"

s = session.post(loginformphpurl, data = params, headers = headers) 

#tracks first redirect after log in. Should be redirected to the page with the "I accept" button

print s.history
try:
    
    if s.history:
        print "Request was redirected"
        for resp in s.history:
            print resp.status_code, resp.url
            print "You are now at:"
            print s.status_code, s.url
    else:
        print "Request was not redirected. You are at:", s.url
        
    print "The cookies are set to:", s.cookies.get_dict()
    print "------"
    
    sleepabit() #pause
    
    #grab ticket data from s.url. The ticket data is generated from the NUS server which is needed for the Lawnet server 
      
    holdingurl = s.url
    print holdingurl
    ticket = ((holdingurl.split("ticket%3D")[1]).split("%2524gCASETRACK"))[0] #extracting ticket string from finalurl
    ticket = ticket.replace("%2524", "%24") #because of the percentage sign being encoded as %25
    
    iAcceptButtonurl = "https://lawproxy1.nus.edu.sg/login?user=nusstu-" + username + "&ticket=" + ticket + "%24gCASETRACK%2BHEINONLINE%2BLAWNET%2BWESTLAW%24e&qurl=http%3A%2F%2Fwww%2Elawnet%2Esg%2Flawnet%2Fip%2Daccess"
    
    acceptInformation = "I Accept"  
    
    #THE BOT IS NOW FACING THE PAGE WITH THE "I ACCEPT" BUTTON. IT WILL NOW MIMICK CLICKING ON THE BUTTON
      
    s = session.post(iAcceptButtonurl, data = acceptInformation, headers = headers) 
    
    #Tracking the second redirect to Lawnet itself
      
    if s.history:
        print "Request was redirected"
        for resp in s.history:
            print resp.status_code, resp.url
            print "You are now at:"
            print s.status_code, s.url
    else:
        print "Request was not redirected. You are at:", s.url
        
    print "The cookies are set to:", s.cookies.get_dict()
    print "------"
    
    sleepabit() #pause
    
    #THE BOT IS NOW LOGGED IN LAWNET AND VIEWING THE HOMEPAGE WITH THE SEARCH BUTTON
    
    #Obtaining the hidden value from the page (circumventing bot prevention measure)
    
    s = session.get(s.url, headers = headers)
    
    bsObj = BeautifulSoup(s.content, "html.parser")
    
    hiddenvalue = (bsObj.find("input", {"name" : "_searchbasicformportlet_WAR_lawnet3legalresearchportlet_formDate"}))["value"]
    
    print "The hidden value is {}".format(hiddenvalue)
    
    #defining the params of the search query
    
    searchBarFormUrl = "https://www-lawnet-sg.lawproxy1.nus.edu.sg/lawnet/group/lawnet/result-page" #this should be where the url the POST request is submitted to... not sure why no PHP/ASP
    
    params2 = {"basicSearchKey": searchTerm, 
               "_searchbasicformportlet_WAR_lawnet3legalresearchportlet_formDate": hiddenvalue,
               "p_p_id": 'legalresearchresultpage_WAR_lawnet3legalresearchportlet', #the params of this line and below are from the url
               "p_p_lifecycle": 1,
               'p_p_state': 'normal',
               "p_p_mode": 'view',
               'p_p_col_id': 'column2',
               'p_p_col_count': 1,
               '_legalresearchresultpage_WAR_lawnet3legalresearchportlet_action': 'basicSeachActionURL',
               '_legalresearchresultpage_WAR_lawnet3legalresearchportlet_searchType': 0,
               "category": specified_resources
    }
    
    #posts the search request with the params + hidden value above
    
    s = session.post(searchBarFormUrl, data = params2, headers = headers) #searchTerm defined at the start

    #tracks the redirect experienced after search
    
    if s.history:
        print "Request was redirected"
        for resp in s.history:
            print resp.status_code, resp.url
            print "You are now at:"
            print s.status_code, s.url
    else:
        print "Request was not redirected. You are at:", s.url
        
    print "The cookies are set to:", s.cookies.get_dict()
    print "------"
    sleepabit()
    
    #THE BOT IS NOW VIEWING THE FIRST PAGE OF THE SEARCH RESULTS

    #I need to grab the searchId from the URL of the results page

    searchId = (s.url).split("legalresearchresultpage_WAR_lawnet3legalresearchportlet_searchId=")[1]
    
    currentPageNumber = 1 

    combinedurl = returnCombinedURL(searchId, 1)

    s = session.get(combinedurl, headers=headers)
    
    #finding the total number of pages of search results before crawling
    
    bsObj = BeautifulSoup(s.content, 'html.parser')
    numberofsearchresults = int(bsObj.find('span', {'class': 'search-result-no'}).get_text()) 
    numberofpages = numberofsearchresults / 10
    if numberofsearchresults % 10 > 0: numberofpages += 1
    
    print "There are {} search results for the term {}".format(numberofsearchresults, searchTerm)
    print "There will be {} number of pages".format(numberofpages)
    
    #STARTS CRAWLING. Visits all the Result Pages in turn, visits all the document urls on each page in turn, downloads all the pages
    
    allURLsofResultPages = returnlistofURLsofResultPages(searchId, numberofpages)
    
    for resultsPageURL in allURLsofResultPages:
        s = session.get(resultsPageURL, headers=headers)
        bsObj = BeautifulSoup(s.content, 'html.parser')
        listofDocumentUrls = returnListofDocumentURLsonResultspage(bsObj)
        
        print 'You are currently on page {} of {}'.format(currentPageNumber, numberofpages)
        currentPageNumber += 1
        
        sleepabit() #Absolutely needed
        
        for documenturl in listofDocumentUrls:
            s = session.get(documenturl, headers=headers)
            bsObj = BeautifulSoup(s.content, 'html.parser')
            nameofcase = bsObj.find('span', {'class': 'caseTitle'}).get_text()
            slr_citation = bsObj.findAll('span', {'class': 'Citation offhyperlink'})
            if slr_citation != []: slr_citation = slr_citation[0].get_text() #because there may not be any slr citation
            neutralcitationofcase = bsObj.findAll('a', {'class': 'pagecontent'})
            if neutralcitationofcase != []: neutralcitationofcase = neutralcitationofcase[0].get_text()
            combinednameofcase = (nameofcase + slr_citation + neutralcitationofcase).encode("utf-8")
            save_object(s.content, (combinednameofcase + ".html"))
            
           
            print "saved case: {}".format(combinednameofcase)
            
            sleepabit() #Absolutely needed
            
    save_object(s.content, "viewofpython.html") #see what the bot last sees before logging out

finally:
    
    #logs out of lawnet
    sleepabit()
    logouturl = 'https://www-lawnet-sg.lawproxy1.nus.edu.sg/lawnet/c/portal/logout?referer=/lawnet/web/lawnet/home'
    s = session.get(logouturl, headers = headers)
    print "You are logged out of lawnet"

