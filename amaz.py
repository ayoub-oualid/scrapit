
from asyncore import write
import csv 
#'''from selenium import webdriver '''
from bs4 import BeautifulSoup
import eel
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
exitFlag=0
def main(recherche):
    driver = webdriver.Edge()
    url ='https://www.amazon.com'
    driver.get(url)
    def get_url(search_term):
        """Generate a url from search term"""
        template = 'https://www.amazon.com/s?k={}&ref=nb_sd_noss_1'
        search_term= search_term.replace(' ','+')
        return template.format(search_term)
    url = get_url(recherche)
    print(url)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    results = soup.find_all('div', {'data-component-type': 's-search-result'})
    len(results)
    item = results[0]
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')
    price_parent = item.find('span' , 'a-price')
    price=price_parent.find('span' , 'a-offscreen').text
    def extract_record(item):
        atag = item.h2.a
        description = atag.text.strip()
        url = 'https://www.amazon.com' + atag.get('href')

        try:
            price_parent = item.find('span' , 'a-price')
            price=price_parent.find('span' , 'a-offscreen').text.replace('$', '')
        except AttributeError:
            return
        result = (description,price,url)
        return result 


    records = []
    results = soup.find_all('div' , {'data-component-type' : 's-search-result'})

    for item in results:
        record = extract_record(item)
        if record: 
            records.append(record)



    

    # def get_url(search_term):
    #     #"""Generate a url from search term"""
    #     template = 'https://www.amazon.com/s?k={}&ref=nb_sd_noss_1'
    #     search_term= search_term.replace('','+')

    #     url = template.format(search_term)

    #     url += '&page{}'

    #     return url


    # for page in range(1,21):
    #     driver.get(url.format(page))
    #     soup = BeautifulSoup(driver.page_source,'html.parser')
    #     results = soup.find_all('div' , {'data-component-type' : 's-search-result'})

    #     for item in results:
    #         record = extract_record(item)
    #         if record:
    #             records.append(record)

    driver.close()

    with open('ama.csv', 'w' ,newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description','Price','Url'])
        writer.writerows(records)
    exitFlag = 1