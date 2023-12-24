import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

driver.get('https://www.linkedin.com/home')
login_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Inicia sesión')]")

wait = WebDriverWait(driver, timeout=2)
wait.until(lambda d : login_btn.is_displayed())
login_btn.click()

username_input = driver.find_element(By.ID, 'username').send_keys('santizu72@gmail.com')
password_input = driver.find_element(By.ID, 'password').send_keys('Secret11.li')
login_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Inicia sesión')]")

wait = WebDriverWait(driver, timeout=2)
wait.until(lambda d : login_btn.is_displayed())
login_btn.click()

cancel = driver.find_element(By.XPATH, "//a[contains(text(), 'Cancelar')]")
wait = WebDriverWait(driver, timeout=2)
wait.until(lambda d : cancel.is_displayed())
login_btn.click()
cancel.click()
time.sleep(20)

