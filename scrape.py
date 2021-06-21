from bs4 import BeautifulSoup
import requests

source=requests.get('https://www.thenetnaija.com/videos/tag/Horror').text

soup=BeautifulSoup(source,'lxml')

content_main=soup.find('div',class_="video-files")


articles =content_main.find_all('article')

for article in articles:

     article_image=article.find('div', class_="thumbnail").img['src']

     article_info=article.find('div',class_="info")

     article_link=article_info.h2.a['href']

     article_name=article_info.h2.a.text

    print(article_image)


    print(article_link)

    print(article_name)

    print()