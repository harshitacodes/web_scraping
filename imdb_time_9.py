import requests,pprint,os.path,json,time,random
from bs4 import BeautifulSoup
from imdb_1 import *
from os import path

def scrape_movie_details(movie_url):

    random_sleep = random.randint(1,3)

    id_movie = ''
    for id_s in movie_url[27:]:
        # print(ids,count)
        # count+=1
        if '/' not in id_s:
            id_movie += id_s
        else:
            break
    file_= id_movie + '.json'


    if path.exists('data_movies/movies_details/' + file_):
        with open('data_movies/movies_details/' + file_, 'r') as data:
            r_file = json.load(data)
        return r_file
    
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
    # return (lists_of_divs)
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


    movie_data_dic = {}

    movie_data_dic['name'] = movie_name
    movie_data_dic['country'] = movie_country
    movie_data_dic['director'] = movie_directors
    movie_data_dic['runtime'] = runtime_movie
    movie_data_dic['genre'] = movie_genre
    movie_data_dic['language'] = movie_language
    movie_data_dic['bio'] = movie_bio
    movie_data_dic['poster_link'] = poster_link


    
    dict_type = json.dumps(movie_data_dic)
    create_file.write(dict_type)
    create_file.close()


    return movie_data_dic

def get_movie_list_details(movies):
    
    scrapped_movies = scrape_top_list()
    movie_list = []
    for i in scrapped_movies:

        Url = scrape_movie_details(i['url'])

        movie_list.append(Url)
    return movie_list
details = get_movie_list_details(scrapped_movies)
# print(details)


