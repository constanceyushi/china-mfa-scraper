# Scrapes bilateral documents from China's Ministry of Foreign Affairs website

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException
)
import time
import pandas as pd
from datetime import datetime

options = webdriver.ChromeOptions()
options.page_load_strategy = 'eager'
options.add_argument('--start-maximized')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
actions = ActionChains(driver)

url='https://www.mfa.gov.cn/web/gjhdq_676201/'
driver.get(url)

documentdict = {
    'region':[],
    'country':[],
    'title':[],
    'year':[],
    'text':[],
    'policy':[],
    'principle':[],
    'link':[]
}

region_data = []
country_data = []

# Step 1: Collect all region URLs from main page
regions = driver.find_elements(By.CSS_SELECTOR, "div.menu ul li a")

for region in regions:
    rurl = region.get_attribute('href')
    rname = region.text
    region_data.append((rname, rurl))

# Step 2: For each region, collect all country URLs
for region_name, regionurl in region_data:
    driver.get(regionurl)
    countries = driver.find_elements(By.CSS_SELECTOR, "ul.clearfix a")
    for country in countries:
        curl = country.get_attribute('href')
        cname = country.text
        country_data.append((region_name, cname, curl))

# Step 3: Extract documents from each country's page
for region_name, country_name, country_url in country_data:
    driver.get(country_url)
    try:
        durl = driver.find_element(By.XPATH, '//a[text()="文件"]')
        durl.click()
    except NoSuchElementException:
        continue

    while True:
        docurls = driver.find_elements(By.CSS_SELECTOR,'div.newsBd a')
        url_list = [docurl.get_attribute('href') for docurl in docurls]
        for url in url_list:
            driver.get(url)

            documentdict['region'].append(region_name)
            documentdict['country'].append(country_name)

            try:
                title = driver.find_element(By.CSS_SELECTOR, 'div.news-title h1').text
                documentdict['title'].append(title)
            except NoSuchElementException:
                try:
                    title = driver.find_element(By.CSS_SELECTOR, 'div.title').text
                    documentdict['title'].append(title)
                except NoSuchElementException:
                    documentdict['title'].append('N/A')

            try:
                rawyear = driver.find_element(By.CLASS_NAME,'time').text
                year = rawyear.split('-')[0]
                documentdict['year'].append(year)
            except NoSuchElementException:
                documentdict['year'].append('N/A')

            try:
                article_text = driver.find_element(By.ID, 'News_Body_Txt_A').text
                documentdict['text'].append(article_text)
            except NoSuchElementException:
                documentdict['text'].append('N/A')

            page_text = driver.find_element(By.TAG_NAME, 'body').text
            # Check if document mentions "One China Policy" or "One China Principle"
            if '一个中国政策' in page_text or '一中政策' in page_text:
                policy = 'Yes'
            else:
                policy = 'No'

            if '一个中国原则' in page_text or '一中原则' in page_text:
                principle = 'Yes'
            else:
                principle = 'No'

            documentdict['principle'].append(principle)
            documentdict['policy'].append(policy)

            link = url
            documentdict['link'].append(link)

            if link[-4:] != '.doc':
                driver.back()
    #loop through all document pages + turn pages

        try:
            next_page = driver.find_element(By.XPATH, '//a[text()="下一页"]')
            href = next_page.get_attribute("href")
            if not href or href == "#":
                break
            next_page.click()
            time.sleep(2)

        except (NoSuchElementException,ElementClickInterceptedException):
            break

df = pd.DataFrame(documentdict)
current_date = datetime.now().strftime('%Y-%m-%d')
df.to_csv(f'mfa_{current_date}.csv', index=False)