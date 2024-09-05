from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from collections import defaultdict
from dotenv import load_dotenv
import os
import re
from helpers.locators import GoogleSearch
from helpers.soup_helper import make_soup
load_dotenv()

CHROMDRIVER = os.getenv('DRIVER_PATH')
gs_locator = GoogleSearch()



def get_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--headless')
    service = Service(CHROMDRIVER)  # Update path to your WebDriver
    driver = webdriver.Chrome(service=service,options=chrome_options)
    return driver


def validate_links(driver,professor_name):
    search_query = f'{professor_name} asu'
    driver.get(f'https://www.google.com/search?q={search_query}')
    extracted_links = driver.find_elements(gs_locator.ALL_LINKS[0],gs_locator.ALL_LINKS[1])
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
    soup = make_soup(driver.page_source)    
    try:
        prof_name = check_if_asuProfile_exists(soup)
        if prof_name is not None:
            prof_name = soup.find('div',class_='person').find('h1',class_='mt-0 mb-3')
        else:
            return None
        department = soup.find('div',class_='primary-dept')
        designation = soup.find('div',class_='primary-title')
        phone = soup.find('a',attrs= {'aria-label': 'Call user'})
        email = soup.find('a', attrs={'aria-label': 'Email user'})
        campus = soup.find('div',class_='campus')
        mail_code = soup.find('div',class_='mail-code')
    except Exception as e:
        print('Error occured,',e)
    result = {
        'Full Name':'' if prof_name is None else prof_name.text,
        'Department':'' if department is None else department.text.strip(),
        'Designation':'' if designation is None else designation.text.strip().replace(',',''),
        'Phone':'' if phone is None else phone.text.strip(),
        'Email':'' if email is None else email.text.strip(),
        'MailCode':'' if mail_code is None else mail_code.text.split(': ')[1],
        'Campus':'' if campus is None else campus.text.split(': ')[1],
    }
    return result

def close_windows(driver):
    while len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    

def check_if_asuProfile_exists(soup):
    profile_exist = soup.find('div',class_='person')
    return profile_exist
        