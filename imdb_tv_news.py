from numpy.core.multiarray import inner
import requests
from bs4 import BeautifulSoup

def get_page_data(url):
    page = requests.get(url)
    if page.status_code == 200:
        return BeautifulSoup(page.text, 'html5lib')
    print('error occurred',page.status_code)

def extract_data(soup):
    section = soup.find('section',{'class':'article listo'})
    articles = section.find_all('article',{'class':'ipl-zebra-list__item news-article'})
    data = [] # list empty
    if len(articles)>0:
        for news in articles:
            title = news.find('h2').text.strip()
            date = news.find('li',{'class':'news-article__date'}).text.strip()
            author = news.find('li',{'class':'news-article__author'}).text.strip()
            source = news.find('li',{'class':'news-article__source'}).text.strip()
            summary = news.find('div',{'class':'news-article__content'}).text.strip()[:100]

            data.append({
                'title':title, 'date':date,
                'author':author, 'source':source,
                'summary':summary
            })
    return data

def save_data(extracted_data, path ):
    import pandas as pd
    df = pd.DataFrame(extracted_data)
    df.to_csv(path, index=None)


soup = get_page_data('https://www.imdb.com/news/tv/?ref_=nv_nw_tv`')
exdata = extract_data(soup)
save_data(exdata, 'datasets/imdb_news.csv')