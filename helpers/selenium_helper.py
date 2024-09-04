from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from collections import defaultdict
from dotenv import load_dotenv
import os
import re

load_dotenv()

CHROMDRIVER = os.getenv('DRIVER_PATH') 



def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    service = Service(CHROMDRIVER)  # Update path to your WebDriver
    driver = webdriver.Chrome(service=service)
    return driver


def validate_links(driver,professor_name):
    
    search_query = f'{professor_name} asu'
    driver.get(f'https://www.google.com/search?q={search_query}')
    extracted_links = driver.find_elements(By.XPATH, "//a[@href]")
    target_matchers = {'asu_profile':r"https:\/\/search\.asu\.edu\/profile\/\d+$",
                       'ratemyprofessor':r"https:\/\/www\.ratemyprofessors\.com\/professor\/\d+$"
                       }
    links=defaultdict()
    for link in extracted_links:
        url = link.get_attribute('href')
        if re.match(target_matchers['asu_profile'],url):
            links['asu_profile'] = url
        elif re.match(target_matchers['ratemyprofessor'],url):
            links['ratemyprofessor'] = url
    return links

def extract_asu_profile(driver,asu_profile_link):
    driver.execute_script("window.open('');")  # Opens a new blank tab
    driver.switch_to.window(driver.window_handles[-1])  # Switch to the newly opened tab
    driver.get(asu_profile_link)
    prof_name=driver.find_element(By.XPATH,"/html/body/div[1]/div/main/div[2]/div[2]/article/div[1]/div/div[2]/h1").get_attribute('innerHTML')
    print(prof_name)
    