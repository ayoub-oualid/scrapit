
from asyncore import write
import csv 
from bs4 import BeautifulSoup
import eel
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
def main(st):
    driver = webdriver.Edge()
    url ='https://www.jumia.ma'
    driver.get(url)
    def get_url(search_term):
        """     global st
        st=search_term """
        """Generate a url from search term"""
        template = 'https://www.jumia.ma/catalog/?q={}'
        search_term= search_term.replace(' ','+')
        url = template.format(search_term)
        url += '&page{}'
        return url



    url = get_url(st)
    def extract_record(item):
        atag = item.a
        soup = BeautifulSoup(driver.page_source,'html.parser')
        results = soup.find_all('article',{'class':'prd _fb col c-prd'})
        #results = soup.find_all('div' , {'class' : '-paxs row _no-g _4cl-3cm-shs'})
        len(results)
        '''
        link = 'https://www.jumia.ma' + atag.get('href')
        description = atag.get('data-name')
        price = atag.get('data-price')
        rat = item.find('div',{'class':'stars _s'}).text
        res = (description,price,rat,link)
        return res'''

        link = 'https://www.jumia.ma' + atag.get('href')
        description = atag.get('data-name')
        price = atag.get('data-price')
        #rat = item.find('div',{'class':'stars _s'}).text
        res = (description,price,link)
        return res


    records = []
    soup = BeautifulSoup(driver.page_source,'html.parser')
    #results = soup.find_all('div' , {'class' : '-paxs row _no-g _4cl-3cm-shs'})
    results = soup.find_all('article',{'class':'prd _fb col c-prd'})
    for item in results:
        record = extract_record(item)
        if record: 
            records.append(record)
    for page in range(1,21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source,'html.parser')
    
        #results = soup.find_all('div' , {'class' : '-paxs row _no-g _4cl-3cm-shs',}).find('article',{'class':'prd _fb col c-prd'})
        results = soup.find_all('article',{'class':'prd _fb col c-prd'})
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)

        driver.close()

        with open('jum.csv', 'w' ,newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Description','Price','Url'])
            writer.writerows(records)
    exitFlag = 1