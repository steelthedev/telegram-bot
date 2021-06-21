from bs4 import BeautifulSoup
import requests


def scraperecent():

    source=requests.get('https://www.thenetnaija.com/videos/tag/Horror').text

    soup=BeautifulSoup(source,'lxml')

    recent_horror=[]

    content_main=soup.find('div',class_="video-files")


    articles =content_main.find_all('article')

    for article in articles:

        
        try:
            article_image=article.find('div', class_="thumbnail").img['src']

            article_info=article.find('div',class_="info")

            article_link=article_info.h2.a['href']

            article_name=article_info.h2.a.text
            
            recent_horror.append({

               'image':article_image,
               'href':article_link,
               'name':article_name
          })

            
        except:
             pass
    return recent_horror


