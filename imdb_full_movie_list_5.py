from imdb_movie_details_4 import *


def get_movie_list_details(movies):
    movie_list = []
    for i in movies[:-1]:
        Url = scrape_movie_details(i['url'])
        movie_list.append(Url)
    return (movie_list)
movie_details = get_movie_list_details(scrape_top_list())
# pprint.pprint(movie_details)