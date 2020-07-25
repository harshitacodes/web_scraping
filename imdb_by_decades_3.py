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
        details = {'position':'','name':'','year':'','rating':'','url':''}
        for i in range(0,len(movies_ranks)):
            details['position'] = int(movies_ranks[i])
            details['name'] = str(movies_name[i])
            year_of_release = release_year[i][1:5]
            details['year'] = int(year_of_release)
            details['rating'] = float(movies_ranting[i])
            details['url'] = movies_url[i]
            All_movies.append(details.copy())

    return All_movies
scrapped_movies = scrape_top_list()

def group_by_year(movies):
    years = []
    for i in movies:
        year = i['year']
        if year not in years:
            years.append(year)
    movies_dict_data = {i:[]for i in years}
    # print(movies_dict_data)
    for i in movies:
        year = i['year']
        for j in movies_dict_data:
            if str(j) == str(year):
                # print(movies_dict_data[j])
                movies_dict_data[j].append(i)
    return movies_dict_data

    # print(years)
grouped_data = group_by_year(scrapped_movies)
# pprint.pprint(grouped_data)


def group_by_decades(movies):

    movies_decades = {}
    unique_year = []
    for index in movies:
        mod = index % 10
        dec = index - mod
        if dec not in unique_year:
            unique_year.append(dec)
    unique_year.sort()

    for i in unique_year:
        movies_decades[i] = []
        print(i)
    for i in movies_decades:
        dec10 = i + 9
        # print(dec10)
        for x in movies:
            # print(x)
            if x <= dec10 and x >= i:
                # print(x)
                for v in movies[x]:
                    # print(4)
                    movies_decades[i].append(v)
 
    # print(unique_year)
    
    return movies_decades
decade = group_by_decades(grouped_data)
pprint.pprint(decade)