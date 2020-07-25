import requests
import pprint
from bs4 import BeautifulSoup

URL = " https://www.imdb.com/india/top-rated-indian-movies/" #url of the imdb.com 
sample = requests.get(URL)

soup = BeautifulSoup(sample.text,"html.parser")


def scrape_top_list():
    m_div = soup.find('div',class_ = 'lister')
    t_body = m_div.find('tbody',class_ = 'lister-list')
    tr_s = t_body.find_all('tr')

    movies_name = []
    movies_ranks = []
    release_year = []
    movies_url = []
    movies_ranting = []

    for tr in tr_s:
        position = tr.find('td', class_ ="titleColumn").get_text().strip()
        rank = ''
        for i in position:
            if '.' not in i:
                rank = rank + i
            else:
                break
        movies_ranks.append(rank)

        title = tr.find('td',class_ ="titleColumn").a.get_text()
        movies_name.append(title)

        years = tr.find('td', class_ ="titleColumn").span.get_text()
        release_year.append(years)

        ratings = tr.find('td', class_ = "ratingColumn").strong.get_text()
        movies_ranting.append(ratings)

        links = tr.find('td', class_ = "titleColumn").a['href']
        movies_link = "https://www.imdb.com" + links
        movies_url.append(movies_link)
        

        All_movies = []
        details = {'position':'','name':'','years':'','rating':'','url':''}
        for i in range(0,len(movies_ranks)):
            details['position'] = int(movies_ranks[i])
            details['name'] = str(movies_name[i])
            year_of_release = release_year[i][1:5]
            details['years'] = int(year_of_release)
            details['rating'] = float(movies_ranting[i])
            details['url'] = movies_url[i]
            All_movies.append(details.copy())

    return All_movies
    # return movies_url

# pprint.pprint(scrape_top_list())
scrapped_movies = scrape_top_list()
# pprint.pprint(scrape[1])
# scrape_top_list()
