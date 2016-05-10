import os.path
import time
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
r = urlopen('https://www.hudhomestore.com/Listing/BidResults.aspx?pageId=1&caseNumber=&zipCode=&city=&county=&sState=IL'
            '&street=&sPageSize=300&OrderbyName=DNETBIDAMOUNT&OrderbyValue=DESC&sLanguage=ENGLISH').read()
soup = BeautifulSoup(r,"lxml")

listhead = soup.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['FormTableSubheader'])

fieldnames = []
for el in listhead:
    if el.a == None:
        fieldnames.append('Property Address')
    else:
        fieldnames.append(el.a.get_text().strip())

listings = soup.find_all(lambda tag: tag.name == 'tr' and (tag.get('class') == ['FormTableRow']) or tag.get('class') == ['FormTableRowAlt'])

dicts = []
for el in listings:
    rawtable_data = el.find_all('td')
    field_data = [x.get_text().strip() for x in rawtable_data]
    data_dict = dict(zip(fieldnames, field_data))
    dicts.append(data_dict)

#f = csv.writer(open("hud_sold" + time.strftime("_%d_%m_%Y") + ".csv", "w"))

output_dir = os.path.expanduser("~")
#file_utils.create_recent_directory(output_dir)
out_path = os.path.join(output_dir, ("hud_sold" + time.strftime("_%d_%m_%Y") + ".csv"))
with open(out_path, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for dict in dicts:
        writer.writerow(dict)
