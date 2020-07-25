from imdb_movie_details import *
from imdb import *
from imdb_full_movie_list import *


def analyse_movies_directors(movies):
    scrapped_movies = scrape_top_list()
    directorss = {}
    for dic in movies_detail:
        directr = dic['director']
        if 1 < len(directr):
            for i in directr:
                if i not in directorss:
                    directorss[i] = 1
                else:
                    directorss[i] += 1
        else:
            if directr[0] not in directorss:
                directorss[directr[0]] = 1
            else:
                directorss[directr[0]] += 1

    return directorss
        
        
    
movies_detail = get_movie_list_details(scrapped_movies[:10])

pprint.pprint(analyse_movies_directors(movies_detail))