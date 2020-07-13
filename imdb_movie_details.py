# import imdb
import requests
from bs4 import BeautifulSoup


def scrape_movie_details(movie_url):
    page = requests.get(movie_url)
    soup = BeautifulSoup(page.text,"html.parser")

    name_row = soup.find('div',class_ = "title_wrapper").h1.get_text()
    # return name_row
    movie_name = ' '
    for i in name_row:
        if '(' not in i:
            movie_name = (movie_name+i).strip()
        else:
            break
    # return movie_name
    sub_div = soup.find('div', class_ = "subtext")
    runtime = sub_div.find('time').get_text().strip()
    # print(type(sub_details))
    runtime_hours = int(runtime[0]) * 60
    movie_runtime = 0
    if 'min' in runtime:
        runtime_min = int(runtime[3:].strip('min'))
        # return runtime_min
        movie_runtime = runtime_hours + runtime_min
    else:
        movie_runtime = runtime_hours

    genre = sub_div.find_all('a')
    genre.pop()

    movie_genre = [i.get_text() for i in genre]
    return movie_genre
    
    # return movie_runtime

    # print(time_hours)
    # return time_hours

url1 = "https://www.imdb.com/title/tt0066763/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=690bec67-3bd7-45a1-9ab4-4f274a72e602&pf_rd_r=8V52MCJ8VG0WN1FX8FZC&pf_rd_s=center-4&pf_rd_t=60601&pf_rd_i=india.top-rated-indian-movies&ref_=fea_india_ss_toprated_tt_6"
print(scrape_movie_details(url1))



 
