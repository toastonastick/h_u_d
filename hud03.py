import re
import os.path
import time
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen
r = urlopen('https://www.hudhomestore.com/Listing/BidResults.aspx?pageId=1&caseNumber=&zipCode=&city=&county=&sState=IL'
            '&street=&sPageSize=200&OrderbyName=DNETBIDAMOUNT&OrderbyValue=DESC&sLanguage=ENGLISH').read()
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

r = urlopen('https://www.hudhomestore.com/Listing/PropertySearchResult.aspx?pageId=1&zipCode='
            '&city=&county=&sState=IL&fromPrice=0&toPrice=0&fCaseNumber=&bed=0&bath=0&street=&buyerType=0'
            '&specialProgram=&Status=0&indoorAmenities=&outdoorAmenities=&housingType=&stories=&parking=&propertyAge='
            '&sPageSize=200&OrderbyName=DLISTPRICE&OrderbyValue=DESC&sLanguage=ENGLISH').read()

soup = BeautifulSoup(r,"lxml")

listhead = soup.find_all(lambda tag: tag.name == 'td' and tag.get('class') == ['FormTableSubheader'])

fieldnames = []
for el in listhead:
    if el.center != None:
        if el.center.get_text().strip() == 'Details':
            break
        else:
            fieldnames.append(el.center.get_text().strip())

listings = soup.findAll(re.compile(r'(label|span)'))

dicts = []
tempdict = {}
for el in listings:
    if el.get('id') != None:
        matchobj = re.match(r'dgPropertyList_ctl(.*)_(.*)', el.get('id'))
    else:
        continue
    if matchobj != None and int(matchobj.group(1)) > 2:
        if matchobj.group(2) == 'Label4':
            tempdict['Property Case'] = el.get_text().strip()
        elif matchobj.group(2) == 'lblAddress':
            tempdict['Address'] = el.get_text().strip()
        elif matchobj.group(2) == 'Label8':
            tempdict['Price'] = el.get_text().strip()
        elif matchobj.group(2) == 'Label2':
            tempdict['Status'] = el.get('title')
        elif matchobj.group(2) == 'Label10':
            tempdict['Bed'] = el.get_text().strip()
        elif matchobj.group(2) == 'Label30':
            tempdict['Bath'] = el.get_text().strip()
        elif matchobj.group(2) == 'Label15':
            tempdict['Listing Period'] = el.get_text().strip()
        elif matchobj.group(2) == 'lblDTBidOpen':
            tempdict['Bid Open Date'] = el.get_text().strip()
        else:
            continue
    if matchobj and matchobj.group(2) == 'lblDTBidOpen':
        dicts.append(tempdict)
        tempdict = {}

output_dir = os.path.expanduser("~")
#file_utils.create_recent_directory(output_dir)
out_path = os.path.join(output_dir, ("hud_initial" + time.strftime("_%d_%m_%Y") + ".csv"))
with open(out_path, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for dict in dicts:
        writer.writerow(dict)
