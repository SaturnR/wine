#!/usr/bin/env python3
import csv
import requests as req
from bs4 import BeautifulSoup

URL = "http://georgianwine.gov.ge/Ge/WineCompaniesAndWineries?page=1&pageSize=2000"

def display(email_divs, limit=None):
    scrap = []
    cnt = 0
    if limit:
        email_divs = email_divs[:limit]
    for info in email_divs:
        links = info.find_all('a')
        email = None
        phone = None
        inform = None
        address = None
        for link in links:
            text = link.text.strip()
            if isEmail(text):
                email = text
            elif isPhoneNumber(text):
                phone = text
        h2 = info.find('h2')
        if h2:
            span = str(h2.find('span'))
            if span:
                inform = str(h2).replace(span,'').strip('<h2>').strip('</h2>')\
                                                               .replace('\t','').replace('\xa0','').strip()
        h3 = info.find('h3')
        if h3:
            address = h3.text.strip()
       
        if phone or email:
            company_info = "Email: {}, Phone {}\nAddress:{}\nInfo: {}".format(email, phone, address, inform)
            scrap.append({'ID':cnt, "email":email, "phone":phone, "address":address, "name":inform})
            cnt+=1
            print(company_info)
        print('\n========================\n')
    return scrap

def isEmail(data):
    if '@' in data[1:-2]:
        return True
    else:
        return False
   
def isPhoneNumber(data):
    for n in data:
        if ord(n) in range(48, 58):
            pass
        else:
            return False
    return True


def toCSV(data):
    with open('wine_companies.csv', mode='w') as wine_file:
        writer = csv.writer(wine_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Address'])
        for comp in data:
            writer.writerow([comp['ID'], comp['name'], comp["email"],
                             comp["phone"], comp["address"]])




if __name__ == "__main__":
    page = req.get(URL)
    html = BeautifulSoup(page.text)
    email_divs = html.findAll("div", {"class": "wineCompanyDesc"})
    company_data = display(email_divs)
    toCSV(company_data)
