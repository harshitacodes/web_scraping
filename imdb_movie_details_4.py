import requests
import pprint
from imdb_1 import *
from bs4 import BeautifulSoup


def scrape_movie_details(movie_url):
    page = requests.get(movie_url)
    soup = BeautifulSoup(page.text,"html.parser")

    name_row = soup.find('div',class_ = "title_wrapper").h1.get_text()
    movie_name = ' '
    for i in name_row:
        if '(' not in i:
            movie_name = (movie_name+i).strip()
        else:
            break
    sub_div = soup.find('div', class_ = "subtext")
    genre = sub_div.find_all('a')
    genre.pop()
    movie_genre = [i.get_text() for i in genre]

    summary = soup.find('div',class_ = 'plot_summary')

    movie_bio =  summary.find('div',class_ = 'summary_text').get_text().strip()
    director = summary.find('div',class_ = 'credit_summary_item')

    director_list = director.find_all('a')
    movie_directors = [i.get_text().strip() for i in director_list]

    extra_movie_details = soup.find('div',attrs={"class":"article","id":"titleDetails"})
    lists_of_divs = extra_movie_details.find_all('div')
    for divs in lists_of_divs:
        h4_tags = divs.find_all('h4')
        for h4 in h4_tags:
            if 'Language:' in h4:
                movie_a_tag = divs.find_all('a')
                movie_language = [Language.get_text() for Language in movie_a_tag]

            elif 'Country:' in h4:
                country_tag = divs.find_all('a')
                movie_country = ''.join([Country.get_text() for Country in country_tag])

            elif 'Runtime:' in h4:
                runtime = divs.find_all('time')
                runtime_movie = ''.join([Runtime.get_text() for Runtime in runtime])


    poster_div_tag = soup.find('div',class_ = "poster").a['href']

    poster_link = "https://www.imdb.com/" + poster_div_tag


    movie_data_dic = {'name':'', 'director':'','country':'','runtime':'','genre':'','language':'','bio':'','poster_link':''}

    movie_data_dic['name'] = movie_name
    movie_data_dic['country'] = movie_country
    movie_data_dic['director'] = movie_directors
    movie_data_dic['runtime'] = runtime_movie
    movie_data_dic['genre'] = movie_genre
    movie_data_dic['language'] = movie_language
    movie_data_dic['bio'] = movie_bio
    movie_data_dic['poster_link'] = poster_link


    return movie_data_dic
  
url1 = scrapped_movies[2]['url']

print(scrape_movie_details(url1))
# pprint.pprint(scrape_movie_details(url1))



 
