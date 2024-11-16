from flask import Flask
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import logging
from flask import request
from flask import render_template
import requests
from flask_cors import CORS,cross_origin
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pymysql
import pandas as pd

logging.basicConfig(filename="C:\\Users\\anshi\\OneDrive\\Desktop\\SIH\\scraper.log",level=logging.INFO)
driver = webdriver.Chrome()

product="googlephone"
link="https://www.flipkart.com/search?q="+product
logging.info(link)

driver.get(link)
time.sleep(1)

outer_html = driver.page_source
with open("page_source.html", "w", encoding="utf-8") as file:
    file.write(outer_html)

try:
    page=bs(outer_html,"html.parser")
    url=page.find_all("a",{"class":"CGtC98"} )
    del url[0:2]
   
    
    pro_link=[]
    for j in url:
        link1="https://www.flipkart.com"+j["href"]
        #logging.info(link1)
        pro_link.append(link1)
    print("No. of links:",len(pro_link))
    
    title=[]
    price=[]
    rating=[]
    image=[]
    for i in pro_link:
    
        driver.get(i)
        outer_html_1 = driver.page_source
      

        a=driver.find_element(By.CLASS_NAME,"VU-ZEz")
        title.append(a.text)
       

        p=driver.find_element(By.CLASS_NAME,"hl05eU")
        pr = p.text.split('₹')[1].split('₹')[0]
        price.append(pr)
        
        
        r=driver.find_element(By.CLASS_NAME,"XQDdHH")
        rating.append(r.text)

        i=driver.find_element(By.CLASS_NAME,"vU5WPQ")
        im=i.find_element(By.TAG_NAME,"img")
        ima=im.get_attribute("src")
        image.append(ima)
       
        
            
            
    logging.info(len(price))
    logging.info(len(rating))
    logging.info(len(image))
except Exception as e:
    print("An error occurred:", e)

df=pd.DataFrame({"product":title,"price":price,"rating":rating,"image_link":image,"product_link":pro_link})
logging.info(df)
df.to_csv("C:\\Users\\anshi\\OneDrive\\Desktop\\sih\\data.csv", index=False)
driver.quit()
