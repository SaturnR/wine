#!/usr/bin/env python3
import re
import csv
import requests as req
from bs4 import BeautifulSoup

URL = "http://georgianwine.gov.ge/Ge/WineCompaniesAndWineries?page=1&pageSize=20"

class Patern:
    EMAIL = '[\w.-]+@[\w.-]+'
    PHONE = '\+*[\d\s-]{4,20}'
    INFO = "[^<h2>]([\w.\s–\-\"',!=])+"

def isEmail(data):
    if re.fullmatch(Patern.EMAIL, data):
        return True
    else:
        return False
   
def isPhoneNumber(data):
    if re.fullmatch(Patern.PHONE, data):
        return True
    else:
        return False

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
        match = re.search(Patern.INFO, str(h2))
        if match:
            inform = match.group()
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

def toCSV(data):
    with open('wine_companies.csv', mode='w') as wine_file:
        writer = csv.writer(wine_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Address'])
        for comp in data:
            writer.writerow([comp['ID'], comp['name'], comp["email"],
                             comp["phone"], comp["address"]])
email_divs = None
company_data = None
if __name__ == "__main__":
    page = req.get(URL)
    html = BeautifulSoup(page.text)
    email_divs = html.findAll("div", {"class": "wineCompanyDesc"})
    company_data = display(email_divs)
    toCSV(company_data)
