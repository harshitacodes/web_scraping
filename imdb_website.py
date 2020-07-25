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
        # print(i)

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
    
    return movies_decades
decade = group_by_decades(grouped_data)
# pprint.pprint(decade)

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
    runtime = sub_div.find('time').get_text().strip()
    runtime_hours = int(runtime[0]) * 60
    movie_runtime = 0
    if 'min' in runtime:
        runtime_min = int(runtime[3:].strip('min'))
        movie_runtime = runtime_hours + runtime_min
    else:
        movie_runtime = runtime_hours

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
            # return movie_country


    poster_div_tag = soup.find('div',class_ = "poster").a['href']

    poster_link = "https://www.imdb.com/" + poster_div_tag


    movie_data_dic = {'name':'', 'director':'','country':'','runtime':'','genre':'','language':'','bio':'','poster_link':''}

    movie_data_dic['name'] = movie_name
    movie_data_dic['country'] = movie_country
    movie_data_dic['director'] = movie_directors
    movie_data_dic['runtime'] = movie_runtime
    movie_data_dic['genre'] = movie_genre
    movie_data_dic['language'] = movie_language
    movie_data_dic['bio'] = movie_bio
    movie_data_dic['poster_link'] = poster_link


    return movie_data_dic
  
url1 = "https://www.imdb.com/title/tt0093603/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=690bec67-3bd7-45a1-9ab4-4f274a72e602&pf_rd_r=BSKKMHJ3ENYSJ925S4Y9&pf_rd_s=center-4&pf_rd_t=60601&pf_rd_i=india.top-rated-indian-movies&ref_=fea_india_ss_toprated_tt_2"


# pprint.pprint(scrape_movie_details(url1))
scrape_movie_details(url1)



def get_movie_list_details(movies):
    
    scrapped_movies = scrape_top_list()
    movie_list = []
    for i in scrapped_movies[:10]:
        Url = scrape_movie_details(i['url'])

        movie_list.append(Url)
    return movie_list
get_movie_list_details(scrape_top_list)


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
analyse_movies_language(movies_detail)


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





