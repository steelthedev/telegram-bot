from bs4 import BeautifulSoup
import requests


def SearchNetnaija(title):


    url = f"https://www.thenetnaija.com/search?folder=videos&t={title}"


    source = requests.get(url).text

    soup = BeautifulSoup(source , "lxml")

    main_content = soup.find('div' , class_="search-results")

    search_result = []

    articles = main_content.find_all("article")

    for article in articles:
        try:

            article_image = article.find("div", class_="thumbnail").img['src']

            article_info = article.find("div", class_="info")

            article_link = article_info.h3.a['href']

            article_name = article_info.h3.a.text

            article_summary = article_info.find("div", class_="excerpt").text

            search_result.append({

                'name': article_name,
                'image':article_image,
                'link': article_link,
                'summary':article_summary,
            })
            
        except:
           pass
    return search_result



def getEpisodes(season_list):
    url = [f"https://kimoitv.com/{season_link['season_link']}" for season_link in season_list]
    e_source = requests.get(url).text
    e_soup = BeautifulSoup(e_source, "lxml")
    epsiode_list[]



def SearchKimoi(title):
    url = f"https://kimoitv.com/search/?q={title}"
    source = requests.get(url).text
    soup = BeautifulSoup(source, "lxml")
    season_list = []
    try:
        movie_url = soup.find("li", class_="mounted").a["href"] 
        movie_full_path = f"https://kimoitv.com/{movie_url}" 
        movie_source = requests.get(movie_full_path).text
        movie_soup = BeautifulSoup(movie_source,"lxml") if movie_source != None else None
        seasons = movie_soup.find("ul", {"class":"link-listview"}) if movie_soup != None else None
        
        for season in seasons:
        
            season_link = season.a["href"]
            season_text= season.a.text.strip()

            season_list.append({
                "season_name":season_text,
                "season_link":season_link
            })
    except:
        pass
    getEpisodes(season_list=season_list)
    return season_list
    
    


    


SearchKimoi("introverted boss")