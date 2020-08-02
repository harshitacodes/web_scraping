from imdb_full_movie_list_5 import *


def analyse_movies_directors_and_languages(movies):
    director_dic = {}
    for movie in movies:
        for director in movie['director']:
            director_dic[director] = {}
    for i in range(len(movies)):
        for director in director_dic:
            if director in movies[i]['director']:
                for language in movies_detail[i]['language']:
                    director_dic[director][language] = 0
    for i in range(len(movies)):
        for director in director_dic:
            if director in movies[i]['director']:
                for language in movies_detail[i]['language']:
                    director_dic[director][language] += 1
    return director_dic

director_details = analyse_movies_directors_and_languages(movies_detail)
print(director_details)