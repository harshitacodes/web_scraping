from imdb_movie_details_4 import *
from imdb_1 import *


def get_movie_list_details(movies):
    
    scrapped_movies = scrape_top_list()
    movie_list = []
    for i in scrapped_movies[:10]:

        Url = scrape_movie_details(i['url'])
        movie_list.append(Url)]
    return (movie_list)
(get_movie_list_details(scrape_top_list))

