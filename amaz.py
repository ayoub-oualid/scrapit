
from asyncore import write
import csv 
#'''from selenium import webdriver '''
from bs4 import BeautifulSoup
import eel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time
exitFlag=0
def main(recherche):
    options = Options()
    options.add_argument("headless")
    driver = webdriver.Edge(options = options)
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
        img1 = item.find('div' , {'class':'a-section aok-relative s-image-square-aspect'})
        img2 = img1.find('img' , {'class':'s-image'})
        img = img2.get('src')
        try:
            price_parent = item.find('span' , 'a-price')
            price=price_parent.find('span' , 'a-offscreen').text.replace('$', '')
        except AttributeError:
            return
        result = (description,price,url,img)
        return result 


    records = []
    results = soup.find_all('div' , {'data-component-type' : 's-search-result'})

    for item in results:
        record = extract_record(item)
        if record: 
            records.append(record)



    
    driver.close()

    with open('ama.csv', 'w' ,newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description','Price','Url','img'])
        writer.writerows(records)
    exitFlag = 1