import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import re
from datetime import datetime, timedelta
import time as timer

# item: {string} url item from soup
def find_biglobe_news_link(item):
    result = re.findall('^https://news.biglobe.ne.jp/[a-z]+/\d{4}/.+\.html$', str(item))
    if result:
        return result[0]
    else:
        return None

def scrape_biglobe():
    today = datetime.today()
    print("-" * 60, 'BogLOBE', "-"*60)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    url = "https://news.biglobe.ne.jp/list/002/969/%E8%A1%8C%E6%94%BF%E6%9B%B8%E5%A3%AB.html"
    res = requests.get(url, headers)
    res.raise_for_status()
    soup = bs(res.content, 'html.parser')

    urls = []
    for item in soup.find_all('a'):
        url = item.get('href')
        result = find_biglobe_news_link(url)
        if result:
            urls.append(str(url))

    news_urls = []
    contents = []
    for url in urls[:10]:
        print(url)
        res = requests.get(url, headers)
        if res.status_code == 200:
            soup = bs(res.content, 'html.parser')
            body = soup.find_all('div', {"class":"news-body"})
            sentences = ''
            for item in body:
                sentence = item.get_text()
                sentence = sentence.replace('\n', '').replace('\u3000', '').replace(' ', '').replace('　', '')
                sentences = sentences + sentence
            news_urls.append(url)
            contents.append(sentences)
        timer.sleep(1)
    
    df = pd.DataFrame({'Url': news_urls, 'Content': contents})
    return df
    
def create_time_list(start):
    end = start - timedelta(days=7)
    current = end
    time_list = []
    while current <= start:
        time_list.append(current)
        current += timedelta(days=1)
    return time_list

def scrape_tabisland():
    today = datetime.today()
    print("-" * 60, 'TabisLand', "-"*60)

    time_list = create_time_list(today)
    url = 'https://www.tabisland.ne.jp/news/'
    types = ['tax', 'management']
    tails = ['_1', '_2', '']
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    
    news_urls = []
    contents = []
    for time in time_list:
        year = time.year
        month = str(time.month) if len(str(time.month)) == 2 else '0' + str(time.month)
        day = str(time.day) if len(str(time.day)) == 2 else '0' + str(time.day) 
        for typ in types:
            for tail in tails:
                news_url = url + f'{typ}/{year}/{month}{day}{tail}.html'
                res = requests.get(news_url, headers)
                timer.sleep(1)
                if res.status_code == 200:
                    print(news_url)
                    soup = bs(res.content, 'html.parser')
                    body = soup.find_all('div', {"class":"news-detail"})
                    sentences = ""
                    for item in body:
                        sentence = item.get_text()
                        sentence = sentence.replace('\n', '').replace('\u3000', '').replace(' ', '').replace('　', '')
                        sentences = sentences + sentence
                    news_urls.append(news_url)
                    contents.append(sentences)

    url = 'https://www.tabisland.ne.jp/column/'
    
    for time in time_list:
        year = time.year
        month = str(time.month) if len(str(time.month)) == 2 else '0' + str(time.month)
        day = str(time.day) if len(str(time.day)) == 2 else '0' + str(time.day) 
        for tail in tails:
            news_url = url + f'/{year}/{month}{day}{tail}.html'
            res = requests.get(news_url, headers)
            timer.sleep(1)
            if res.status_code == 200:
                print(news_url)
                soup = bs(res.content, 'html.parser')
                body = soup.find_all('div', {"class":"column-detail"})
                sentences = ""
                for item in body:
                    sentence = item.get_text()
                    sentence = sentence.replace('\n', '').replace('\u3000', '').replace(' ', '').replace('　', '')
                    sentences = sentences + sentence
                news_urls.append(news_url)
                contents.append(sentences)

    df = pd.DataFrame({'Url': news_urls, 'Content': contents})
    return df



# item: {string} url item from soup
def find_yahoo_news_link(item):
    result = re.findall('^https://news.yahoo.co.jp/articles/.+', str(item))
    if result:
        return result[0]
    else:
        return None



def scrape_yahoo_news(query_param=None):
    today = datetime.today()
    print("-" * 60, 'Yahoo News', "-"*60)

    if query_param:
        base = 'https://news.yahoo.co.jp/search?p='
        base_urls = []
        for q in query_param:
            base_urls.append(base+str(q))
    else:
        base_urls = ['https://news.yahoo.co.jp/search?p=%E8%A1%8C%E6%94%BF%E6%9B%B8%E5%A3%AB&ei=UTF-8', # 行政書士
                'https://news.yahoo.co.jp/search?p=%E5%AE%B6%E6%97%8F%E3%80%80%E4%BF%A1%E8%A8%97&ei=utf-8&aq=1', # 家族 信託
                'https://news.yahoo.co.jp/search?p=%E9%81%BA%E8%A8%80%E6%9B%B8&ei=utf-8&aq=2']          # 遺言書
    
    urls = []
    print(base_urls)
    for base_url in base_urls:
        # get news urls 
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        res = requests.get(base_url, headers)
        res.raise_for_status()
        soup = bs(res.content, 'html.parser')

        count = 0
        for item in soup.find_all('a'):
            url = item.get('href')
            #print(url)
            result = find_yahoo_news_link(url)
            if result:
                urls.append(str(url))
                count += 1
            if count == 10:
                break
    pages = ['?page=1', '?page=2', '?page=3', '?page=4']

    news_urls = []
    contents = []
    for url in urls:
        for page in pages:
            news_url = url + page
            res = requests.get(news_url, headers)
            timer.sleep(1)
            if res.status_code == 200:
                print(news_url)
                soup = bs(res.content, 'html.parser')
                body = soup.find_all('p', {"class": "yjSlinkDirectlink"})
                sentences = ""
                for item in body:
                    sentence = item.get_text()
                    sentence = sentence .replace('\n', '').replace('\u3000', '').replace(' ', '').replace('　', '')
                    sentences += sentence
                news_urls.append(news_url)
                contents.append(sentences)
        
    df = pd.DataFrame({'Url': news_urls, 'Content': contents})
    return df


# item: {string} url item from soup
def find_rakuten_news_link(item):
    result = re.findall('^/article/.+', str(item))
    if result:
        return result[0]
    else:
        return None


def scrape_rakuten_infoseek(query_param=None):
    today = datetime.today()
    print("-" * 60, 'Rakuten InfoSeek', "-"*60)

    # get news urls 
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}


    if query_param:
        base = 'https://news.infoseek.co.jp/search?type=article&q='
        base_urls = []
        for q in query_param:
            base_urls.append(base+str(q))
    else:
        base_urls = ['https://news.infoseek.co.jp/search?type=article&q=%E8%A1%8C%E6%94%BF%E6%9B%B8%E5%A3%AB',               # 行政書士
                    'https://news.infoseek.co.jp/search/?type=article&q=%E5%AE%B6%E6%97%8F%E3%80%80%E4%BF%A1%E8%A8%97',     # 家族 信託
                    'https://news.infoseek.co.jp/search/?type=article&q=%E9%81%BA%E8%A8%80%E6%9B%B8']                      # 遺言書
        
    urls = []
    print(base_urls)
    pages = ['&p=1']
    for base_url in base_urls:
        for page in pages:
            page_url = base_url + page
            res = requests.get(page_url, headers)
            timer.sleep(1)
            if res.status_code == 200:
                soup = bs(res.content, 'html.parser')
                for item in soup.find_all('a'):
                    article_url = item.get('href')
                    result = find_rakuten_news_link(article_url)
                    if result:
                        urls.append(str(article_url))

    base_url = 'https://news.infoseek.co.jp'

    news_urls = []
    contents = []
    for url in urls:
        news_url = base_url + url
        res = requests.get(news_url, headers)
        timer.sleep(1)
        if res.status_code == 200:
            print(news_url)
            soup = bs(res.content, 'html.parser')
            body = soup.find_all('div', {"class":"topic-detail__text"})
            sentences = ""
            for item in body:
                sentence = item.get_text()
                sentence = sentence.replace('\n', '').replace('\u3000', '').replace(' ', '').replace('  ', '')
                sentences += sentence
            news_urls.append(news_url)
            contents.append(sentences)

    df = pd.DataFrame({'Url': news_urls, 'Content': contents})
    return df


# 実行
def scrape_to_df(query_param=None):
    biglobe_df = scrape_biglobe()
    tabisland_df = scrape_tabisland()
    yahoo_df = scrape_yahoo_news(query_param)
    rakuten_df =  scrape_rakuten_infoseek(query_param)

    df_list = [biglobe_df, tabisland_df, yahoo_df, rakuten_df]
    df = pd.concat(df_list)
    
    return df

if __name__ == '__main__':
    scrape_to_df()