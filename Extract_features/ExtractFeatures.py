import re
import time
import bs4
from urllib.parse import urlparse
import ipaddress
import tldextract
from bs4 import BeautifulSoup, Comment
from pyparsing import empty
from tldextract import extract
from Extract_features.RobotsValidate import *
import requests
from datetime import datetime
import whois
from math import log2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from Environment.path import driver_path

def Long_URL(url):
    URLLength = len(url)
    if URLLength > 45:
        return 1
    else:
        return 0

def getDomain(url):
    try:
        Domain = urlparse(url).netloc
    except:
        return 'invalid url'
    return Domain

def isDomainIP(domain):
    try:
        ipaddress.ip_address(domain)
        return 1
    except:
        return 0


import re


def shorten_url(url):
    pattern = re.compile(r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                         r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                         r'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                         r'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                         r'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                         r'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                         r'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                         r'tr\.im|link\.zip\.net', re.IGNORECASE)

    # Match the URL using the regex pattern
    match = re.search(pattern, url)

    # Return 1 if match is found, otherwise return 0
    return 1 if match else 0


def No_of_subdomain(url):
    extracted = tldextract.extract(url)
    subDomain = extracted.subdomain.split('.')
    No_subdomain = len([part for part in subDomain if part])
    if No_subdomain < 0:
        No_subdomain = 0
    return No_subdomain

def No_special_char(url):
    if url.startswith('http://'):
        url = url[len('http://'):]
    elif url.startswith('https://'):
        url = url[len('https://'):]
    no_special = 0
    for char in url:
        if not char.isalnum():
            no_special += 1
    return no_special

def isHTTPS(url):
    if url.startswith('https://'):
        return 1
    else:
        return 0

def DomainEntropy(domain):
    entropy = 0
    domain_length = len(domain)
    char_count = {}
    for char in domain:
        char_count[char] = char_count.get(char, 0) + 1

    for count in char_count.values():
        prob_char = count / domain_length
        entropy -= prob_char * log2(prob_char)

    if round(entropy, 2) >= 3.50:
        return 1
    else:
        return 0

"""
-----------Crawling from here-----------
"""

def No_JS(no_js):
    if no_js > 4:
        return 1
    else:
        return 0

def No_CSS(no_css):
    if no_css > 5:
        return 1
    else:
        return 0

def No_ref(no_selfRef, no_emptyRef, no_externalRef):
    Ref = []
    if no_selfRef > 10:
        Ref.append(1)
    else:
        Ref.append(0)

    if no_emptyRef > 3:
        Ref.append(1)
    else:
        Ref.append(0)

    if no_externalRef > 5:
        Ref.append(1)
    else:
        Ref.append(0)

    return Ref

def Crawl(url):
    service = Service(executable_path = driver_path)
    options = Options()
    options.add_argument('--headless')  # Optional: Run in headless mode
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service = service, options = options)

    try:
        driver.get(url)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        webpage = driver.page_source
        soup = BeautifulSoup(webpage, 'lxml')

        # Extract features
        hasTitle = int(bool(soup.find('title') and soup.find('title').text.strip()))
        hasDescription = int(bool(soup.find('meta', attrs={'name': 'description'}) or
                                  soup.find('meta', attrs={'property': 'og:description'})))

        no_js = len(soup.find_all('script'))
        no_css = len(soup.find_all('link', rel='stylesheet')) + len(soup.find_all('style'))
        no_selfRef = len(soup.find_all('a', href='/'))
        no_emptyRef = len(soup.find_all('a', href='#'))
        no_externalRef = sum(1 for a in soup.find_all('a', href=True) if a['href'].startswith(('http://', 'https://')))

        js = No_JS(no_js)
        css = No_CSS(no_css)
        ref = No_ref(no_selfRef, no_emptyRef, no_externalRef)
        selfRef = ref[0]
        emptyRef = ref[1]
        externalRef = ref[2]

        return hasTitle, hasDescription, js, css, selfRef, emptyRef, externalRef
    except WebDriverException as e:
        print(f"WebDriver error: {e}")
        return [0] * 7
    finally:
        driver.quit()

def Whois(domain):
    whois_info = whois.whois(domain)
    current_date = datetime.now()
    creation_date = whois_info.creation_date
    domain_age = 0
    if creation_date is not None:
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if isinstance(creation_date, datetime):
            domain_age = (current_date - creation_date).days / 365
    return domain_age

def feature_extraction_crawl(url):
    feature: list = []
    domain = getDomain(url)
    feature.append(Long_URL(url))
    # feature.append(getDomain(url))
    feature.append(isDomainIP(domain))
    feature.append(shorten_url(url))
    feature.append(No_of_subdomain(url))
    feature.append(No_special_char(url))
    feature.append(isHTTPS(url))
    feature.append(DomainEntropy(domain))

    hasRobot, isAllow, crawl_delay = checkRobot(url)
    if hasRobot == 1 and isAllow == 1:
        hasTitle, hasDescription, js, css, selfRef, emptyRef, externalRef = Crawl(url)
    else:
        hasTitle = hasDescription = js = css = selfRef = emptyRef = externalRef = 0

    feature.append(hasTitle)
    feature.append(hasRobot)
    feature.append(hasDescription)
    feature.append(css)
    feature.append(js)
    feature.append(selfRef)
    feature.append(emptyRef)
    feature.append(externalRef)
    return feature, isAllow