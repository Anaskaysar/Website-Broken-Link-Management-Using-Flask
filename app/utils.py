# app/utils.py
import requests
from bs4 import BeautifulSoup
from .models import BrokenLink, SpamReport
from . import db
import re

def extract_urls_from_page(content):
    soup = BeautifulSoup(content, 'html.parser')
    urls = []
    for link in soup.find_all('a', href=True):
        urls.append(link['href'])
    return urls

def check_url_status(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code
    except requests.RequestException:
        return 'Error'

def detect_spam(content):
    spam_keywords = ['buy now', 'free', 'click here', 'subscribe', 'winner']
    pattern = re.compile('|'.join(spam_keywords), re.IGNORECASE)
    if pattern.search(content):
        return True, 'Contains spam keywords'
    return False, ''
