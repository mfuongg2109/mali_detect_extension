import random
import urllib.robotparser
from urllib.parse import urlparse, urljoin
import requests

def checkConnection(url):
    try:
        webpage = requests.get(url, timeout = 5)
        return 1
    except requests.exceptions.RequestException:
        return 0

def checkRobot(url):
    parsed_url = urlparse(url)
    robots_url = urljoin(f"{parsed_url.scheme}://{parsed_url.netloc}", '/robots.txt')
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    isRobot = 1
    try:
        rp.read()
        if rp.read():
            print('Successfully find robots.txt')
    except Exception as e:
        print(f"Error reading robots.txt from {robots_url}: {e}")
        isRobot = 0
        return isRobot, 0, random.randint(5, 15)

    isAllow = rp.can_fetch('*', url)
    if isAllow:
        isAllow = 1
    else:
        isAllow = 0

    if isAllow == 1:
        crawl_delay = rp.crawl_delay('*')
        if crawl_delay is None:
            crawl_delay = random.randint(5, 15)
    else:
        crawl_delay = random.randint(5, 15)

    return int(isRobot), int(isAllow), int(crawl_delay)