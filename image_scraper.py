# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 08:14:25 2023

@author: Lillemoen
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
from fake_useragent import UserAgent
import time
import random

df = pd.read_csv('filtered_pivot_table.csv')
ua = UserAgent(min_percentage=1.3)

def fetch_name(amazon_code):

    headers = {"User-Agent":ua.random, "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    
    html_review_text = requests.get('https://www.amazon.co.uk/gp/aw/cr/' + amazon_code, headers=headers).text
    review_soup = BeautifulSoup(html_review_text, 'lxml')
    
    author_element = review_soup.find('span', id='cr-arp-byline')
    if author_element:
        author = author_element.find('a').text
    else:
        author = ""
    
    item_tag = review_soup.find('a', {"data-hook":"product-link"})
    if item_tag:
        item_link = "https://www.amazon.co.uk" + item_tag['href']
        item_text = item_tag.text
        return item_text, item_link, author
    else:
        return "", "", ""

def fetch_image_url(query):
    url = f"https://www.google.com/search?tbm=isch&q={query.replace(' ', '+')}"
    headers = { #random header doesn't seem to work on google
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    image_element = soup.find('img', class_="DS1iW")
    if image_element:
        image_url = image_element['src']
        return image_url
    else:
        return ""
    
# Function to truncate strings to 80 characters at the last whitespace
def truncate_string(text, length):
    if len(str(text)) <= length:
        return text
    else:
        return str(text)[:text.rfind(' ', 0, length)]

# # item_text = fetch_name('038568231X')
# # image_url = fetch_image_url(item_text + " Book")

info_df = pd.DataFrame({
    'item_code': [],
    'item_name': [],
    'item_author': [],
    'image_url': [],
    'amazon_link': []
})

for col in df.columns[1:]:
    name, link, author = fetch_name(col)
    url = fetch_image_url(name + " Book")
    info_df = info_df.append({
        'item_code': col,
        'item_name': name,
        'item_author': author,
        'image_url': url,
        'amazon_link': link
    }, ignore_index=True)
    time.sleep(random.randint(0, 3))
    
SPECIFIED_LENGTHS = {'item_name': 80, 'item_code': 50, 'item_author': 50}

#Trim columns to specificed lengths for SQL database    
for col, length in SPECIFIED_LENGTHS.items():
    df[col] = df[col].apply(truncate_string, args=(length,))
    
#Excel doesn't like certain symbols from scraping so need to replace them
df['item_name'] = df['item_name'].str.replace("‘", "'").str.replace("’", "'").str.replace("—", "-").str.replace("–", "-")
    
df.to_csv('book_info.csv')


