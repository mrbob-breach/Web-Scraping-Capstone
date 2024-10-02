from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

RENTAL_URL = "https://appbrewery.github.io/Zillow-Clone/"
GOOGLE_FORM = "https://forms.gle/J3QcHV8fmfzRf9G36"


"""Use BeautifulSoup to get listing information from Zillow Clone site"""
response = requests.get(
    RENTAL_URL,
    headers={
        "Accept-Language":"en-US,en;q=0.9",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
)
soup = BeautifulSoup(response.text, "html.parser")

listing_addresses = [listing.getText().strip().replace('|', '')
                     for listing in soup.find_all('a', class_='StyledPropertyCardDataArea-anchor')]
listing_prices = [re.sub('[^0-9,]', '', listing.getText()[:6])
                  for listing in soup.find_all('span', class_='PropertyCardWrapper__StyledPriceLine')]
listing_links = [listing.get('href') for listing in soup.find_all('a', class_='StyledPropertyCardDataArea-anchor')]

"""Use Selenium to fill in Google Form with listing information"""
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(GOOGLE_FORM)

for listing in range(len(listing_addresses)):

    time.sleep(.5)
    address_fill = driver.find_element(By.XPATH, "//input[@aria-labelledby='i1']")
    price_fill = driver.find_element(By.XPATH, "//input[@aria-labelledby='i5']")
    link_fill = driver.find_element(By.XPATH, "//input[@aria-labelledby='i9']")
    submit_button = driver.find_element(By.CLASS_NAME, "uArJ5e")
    time.sleep(.5)

    address_fill.send_keys(listing_addresses[listing])
    price_fill.send_keys(listing_prices[listing])
    link_fill.send_keys(listing_links[listing])
    submit_button.click()
    time.sleep(.5)

    submit_another = driver.find_element(By.LINK_TEXT, "Submit another response")
    submit_another.click()
