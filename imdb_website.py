import requests
import pprint
import os.path
import random
import time
import json
from bs4 import BeautifulSoup

URL = " https://www.imdb.com/india/top-rated-indian-movies/" #url of the imdb.com 
sample = requests.get(URL)

soup = BeautifulSoup(sample.text,"html.parser")

# task 1
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
        details = {}
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

#
#task 4 and 8,9
def scrape_movie_details(movie_url):
    movie_data_dic = {}

    #task 9
    random_sleep = random.randint(1,3)

    id_movie = ''
    for id_s in movie_url[27:]:
        if '/' not in id_s:
            id_movie += id_s
        else:
            break
    file_= id_movie + '.json'


    text = None

    if os.path.exists('data_movies/movies_details/' + file_):
        fi_ = open('data_movies/movies_details/' + file_)
        r_file = fi_.read()
        j_loads = json.loads(r_file)
        return j_loads

    if text is None:
    
        create_file = open('data_movies/movies_details/' + file_ , 'w')

        time.sleep(random_sleep)

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

        run_time = sub_div.find('time').get_text().strip()
        runTime_hours = int(run_time[0]) * 60
        movie_runtime = 0
        if 'min' in run_time:
            runtime_min = int(run_time[3:].strip('min'))  
            movie_runtime = runTime_hours + runtime_min
        else:
            movie_runtime = runTime_hours 
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

        poster_div_tag = soup.find('div',class_ = "poster").a['href']

        poster_link = "https://www.imdb.com/" + poster_div_tag


        movie_data_dic = {}

        movie_data_dic['name'] = movie_name
        movie_data_dic['country'] = movie_country
        movie_data_dic['director'] = movie_directors
        movie_data_dic['runtime'] = movie_runtime
        movie_data_dic['genre'] = movie_genre
        movie_data_dic['language'] = movie_language
        movie_data_dic['bio'] = movie_bio
        movie_data_dic['poster_link'] = poster_link

        
        dict_type = json.dumps(movie_data_dic)
        create_file.write(dict_type)
        create_file.close()


        return movie_data_dic
# pprint.pprint(scrape_movie_details(scrapped_movies[0]['url']))


#task 5
def get_movie_list_details(movies):
    movie_list = []
    for i in movies[:10]:
        Url = scrape_movie_details(i['url'])
        movie_list.append(Url)
    return (movie_list)
movies_details = get_movie_list_details(scrape_top_list())
# pprint.pprint(movies_details)

# #task 10

def analyse_movies_directors_and_languages(movies):
    director_dic = {}
    for movie in movies:
        for director in movie['director']:
            director_dic[director] = {}
    for i in range(len(movies)):

        for director in director_dic:
            if director in movies_details[i]['director']:
                for language in movies_details[i]['language']:
                    director_dic[director][language] = 0

    for i in range(len(movies)):
        for director in director_dic:
            if director in movies[i]['director']:
                for language in movies_details[i]['language']:
                    director_dic[director][language] += 1
    return director_dic

director_details = analyse_movies_directors_and_languages(movies_details)
# print(director_details)

# #task 11

def analyse_movies_genre(movies):
    genre_dic = {}
    for gen in movies:
        genre_key = gen['genre']
        if 1 < len(genre_key):
            for i in genre_key:
                if i not in genre_dic:
                    genre_dic[i] = 1
                else:
                    genre_dic[i]+=1
        else:
            if genre_key[0] not in genre_dic:
                genre_dic[genre_key[0]] = 1
            else:
                genre_dic[genre_key[0]] += 1
    return genre_dic


genre_details = analyse_movies_genre(movies_details)

#task 12

def scrape_movie_cast(movie_cast_url):


    url_id = movie_cast_url[27:36]

    text = None

    if os.path.exists('cache_file_id/'+ str(url_id) + '.json'):
        open_file = open('cache_file_id/' + str(url_id) + '.json')
        read_file = open_file.read()
        json_data = json.loads(read_file)
     
        return json_data
    
    else:
        url_ = movie_cast_url
        response = requests.get(url_)
        soup = BeautifulSoup(response.text,'html.parser')

        table_tag = soup.find('table',class_ = 'cast_list')

        tbles = table_tag.findAll('td',class_ = '')

        cast_list = []

        for actor in tbles:
            dict_id_actor = {}
            imdb_id = actor.find('a').get('href')[6:15]
            actor_name = actor.get_text().strip()
            dict_id_actor['imdb_id'] = str(imdb_id) 
            dict_id_actor['actor'] = str(actor_name)
            cast_list.append(dict_id_actor)
        
        json_data = cast_list
        
        with open('cache_file_id/' + str(url_id) + '.json', 'w+') as f:
            json.dump(json_data,f)
    return cast_list
cast_url = "https://www.imdb.com/title/tt0066763/fullcredits?ref_=tt_cl_sm#cast"

scrape_movie_cast(cast_url)


# #task 13
def scrape_movie_details_cast(movie_url):
    m_url = movie_url[:37]

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
    run_time = sub_div.find('time').get_text().strip()
    runTime_hours = int(run_time[0]) * 60
    movie_runtime = 0
    if 'min' in run_time:
        runtime_min = int(run_time[3:].strip('min'))  
        movie_runtime = runTime_hours + runtime_min
    else:
        movie_runtime = runTime_hours
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


    poster_div_tag = soup.find('div',class_ = "poster").a['href']

    poster_link = "https://www.imdb.com/" + poster_div_tag


    movie_data_dic = {}

    movie_data_dic['name'] = movie_name
    movie_data_dic['country'] = movie_country
    movie_data_dic['director'] = movie_directors
    movie_data_dic['runtime'] = movie_runtime
    movie_data_dic['genre'] = movie_genre
    movie_data_dic['language'] = movie_language
    movie_data_dic['bio'] = movie_bio
    movie_data_dic['poster_link'] = poster_link

    cast_data = scrape_movie_cast(m_url)
    movie_data_dic['cast'] = cast_data


    return movie_data_dic
# pprint.pprint(scrape_movie_details(scrapped_movies[0]['url']))

cast_dic_data = []

for i in scrapped_movies[:10]:
    url = i['url']
    cast_dic_data.append(scrape_movie_details_cast(url))
    # print(cast_dic_data)

#task 15

def analyse_actors(movies):
    actors_data = {}
    for i in movies:
        cas = i['cast']
        for j in cas:
            caste_id = j['imdb_id']
            caste_name = j['actor']
            if caste_id in actors_data:
                data_dic['num_movie'] +=  1
            else:
                actors_data[caste_id] = {}
                data_dic =  actors_data[caste_id]
                data_dic['name'] = caste_name
                data_dic['num_movie'] = 1
    return  actors_data     
(analyse_actors(cast_dic_data))