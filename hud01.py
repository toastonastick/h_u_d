import time
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
r = urlopen('https://www.hudhomestore.com/Listing/BidResults.aspx?pageId=1&caseNumber=&zipCode=&city=&county=&sState=IL'
            '&street=&sPageSize=300&OrderbyName=DNETBIDAMOUNT&OrderbyValue=DESC&sLanguage=ENGLISH').read()
soup = BeautifulSoup(r,"lxml")

date_str = time.strftime("_%d_%m_%Y")
f = csv.writer(open("hud_sold" + date_str + ".csv", "w"))

listhead = soup.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['FormTableSubheader'])
lst = []
for el in listhead:
  if el.a != None:
      lst.append(el.a.get_text().strip())

lst.insert(1,"Property Address")   #skips for some reason

f.writerow(lst)    # Write column headers as the first line

listings = soup.find_all(lambda tag: tag.name == 'tr' and (tag.get('class') == ['FormTableRow']) or tag.get('class') == ['FormTableRowAlt'])

for el in listings:
    lst1 = []
    for elms in el.find_all('td'):
        lst1.append(elms.get_text().strip())
    f.writerow(lst1)
