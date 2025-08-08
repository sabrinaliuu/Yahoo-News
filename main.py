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
driver.get('https://news.yahoo.co.jp/search?p='+keywords+'&ei=utf-8') # put the url you want to get # go to this page


## 2. Load existing news articles ##
##### loading folded posts -> もっと見る #####
# feature #
# 1) you need to click "もっと見る" to load more news
# 2) the maximun for "もっと見る" is 20 times
page_count = 1
while True: #page_count<6:
    print(page_count)
    try:
        motto_bttn  = driver.find_element(By.CLASS_NAME, "sc-1hdlpx9-1.hzrbWI") # find button
        motto_bttn.click() # click the button
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll down
        time.sleep(8) # wait for 8 seconds (loading)
        page_count += 1
        
        if page_count%10 == 0:
            time.sleep(5)
    except:
        print("no further posts")
        break

## 3. Get news articls list ##
##### get titles & urls #####
soup = BeautifulSoup(driver.page_source, 'lxml') # get the page
rows = soup.find_all('li',class_=re.compile("sc-1u4589e-0 kKmBYF")) # find all news
titles = list()
urls = list()
times = list()
for r in rows: # get title, url for all news by row (by element li)
    title = r.find(class_="sc-3ls169-0 sc-110wjhy-2 dHAJpi dKognN").text
    url = r.find('a').get('href') # save url # important !! # you need this to go into each news article's page
    time_ = r.find('time').text
    titles.append(title)
    urls.append(url)
    times.append(time_)

post_num = len(titles)

## 4. get the full articles by the news list ##
##### load each post by collected urls #####
posts = list()
ids = list()
titles_new = list()
urls_new = list()
times_new = list()

error_url = list() # record error articles


for p_num in range(0,post_num): 
    
    print(p_num)
    
    try:
        post_new = '' 
        u = urls[p_num] # load each url
        driver.get(u) # go to the page by url
        soup_each = BeautifulSoup(driver.page_source, 'lxml')
        pages = soup_each.find_all(class_="sc-qkog50-0 lfMsek") # check how many pages for this news articles
        page_num = 1 if len(pages)==0 else len(pages)
        
        for page in range(1,page_num+1): # load all texts for each page for this news articles

            driver.get(u+'?page='+str(page))
            time.sleep(8) # wait
            soup_each = BeautifulSoup(driver.page_source, 'lxml')
                
            post = soup_each.find_all(class_="sc-54nboa-0 deLyrJ yjSlinkDirectlink highLightSearchTarget")#"article_body highLightSearchTarget").text#"sc-54nboa-0 deLyrJ yjSlinkDirectlink highLightSearchTarget").text
            for p in post:
                post_new = post_new + p.text + '\n\n' # combine texts
 
        times_new.append(times[p_num])
        urls_new.append(urls[p_num])
        titles_new.append(titles[p_num])
        posts.append(post_new)
        ids.append(urls[p_num].split('articles/')[1])
        time.sleep(2)
    except:
        print(titles[p_num])
        print(urls[p_num].split('articles/')[1])
        error_url.append(urls[p_num])
    
    if p_num%10 == 0:
        time.sleep(10)
    
## 5. Save the data ##
import csv

data = {
    "id": ids,
    "title": titles_new,
    "url": urls_new,
    "time": times_new,
    "post": posts
}

## save csv file ##
with open('./output.csv', 'w', newline='', encoding='UTF-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['id','title', 'url','time','post'])
    
    for i in range(len(data['id'])):
        output_row = [data['id'][i], data['title'][i], data['url'][i] ,data['time'][i], data['post'][i]]
        writer.writerow(output_row)

## or save json file ##
import json
pd.DataFrame(data).to_json("output.json", orient="records", force_ascii=False, indent=5)
