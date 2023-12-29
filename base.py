import time
import random

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

SEARCH = {
    'python': 'https://www.linkedin.com/jobs/search?keywords=Python&location=Spain&geoId=105646813&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
    'javascript': 'https://www.linkedin.com/jobs/search?keywords=JavaScript&location=Spain&geoId=105646813&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
    'java': 'https://www.linkedin.com/jobs/search?keywords=JavaScript&location=Spain&geoId=105646813&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
    'php': 'https://www.linkedin.com/jobs/search?keywords=php&location=Espa%C3%B1a&geoId=105646813&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
}

driver = webdriver.Chrome()

url = random.choice(SEARCH)
driver.get(url)

time.sleep(20)

