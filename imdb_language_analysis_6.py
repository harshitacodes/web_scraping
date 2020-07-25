from imdb import *
from imdb_movie_details import *
from imdb_full_movie_list import *

def analyse_movies_language(movies):
    scrapped_movies = scrape_top_list()
    movies_detail = get_movie_list_details(scrapped_movies[:10])
    count_lan = {}
    for lan in movies_detail:
        lan1= lan['language']
        if 1<len(lan1):
            for i in lan1:
                if i not in count_lan:
                    count_lan[i]=1
                else:
                    count_lan[i]+=1
        if lan1[0] not in count_lan:
            count_lan[lan1[0]]=1
        else:
            count_lan[lan1[0]]+=1
    return count_lan
movies_detail = get_movie_list_details(scrapped_movies[:10])   
print(analyse_movies_language(movies_detail))