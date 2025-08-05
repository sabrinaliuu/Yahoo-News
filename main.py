from selenium import webdriver # for controlling website
from bs4 import BeautifulSoup # get html elements
import time
from selenium.webdriver.common.by import By 
import re
import pandas as pd

## 1. Define ##
##### set searching keywords #####
keywords = '能登半島地震+復興'

##### start controlled mode #####
driver = webdriver.Chrome()
driver.get('https://news.yahoo.co.jp/search?p='+keywords+'&ei=utf-8') # put the url you want to get


## 2. Get existing news list ##
##### loading folded posts -> もっと見る #####
# feature #
# 1) you need to click "もっと見る" to load more news
# 2) the maximun for "もっと見る" is 20 times
page_count = 1
while True: #True:
    print(page_count)
    try:
        motto_bttn  = driver.find_element(By.CLASS_NAME, "sc-1hdlpx9-1.hzrbWI")
        motto_bttn.click()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(8)
        page_count += 1
        
        if page_count%10 == 0:
            time.sleep(5)
    except:
        print("no further posts")
        break

