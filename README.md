# IMDb Top Rated Indian Movies Scraper

This script scrapes the list of top-rated Indian movies from IMDb's website and retrieves details such as movie name, rank, release year, rating, and IMDb URL.

## Overview

This Python script utilizes BeautifulSoup and requests libraries to fetch and parse data from IMDb's top-rated Indian movies webpage. It extracts information from each movie entry in the list and structures it into a list of dictionaries containing movie details.

## How It Works

The script performs the following steps:

1. **Fetching Data**: It sends a request to IMDb's top-rated Indian movies webpage (`https://www.imdb.com/india/top-rated-indian-movies/`).

2. **Parsing HTML**: It uses BeautifulSoup to parse the HTML content of the webpage.

3. **Extracting Movie Details**: It locates the relevant HTML elements containing movie details such as name, rank, release year, rating, and IMDb URL.

4. **Formatting Data**: It structures the extracted information into a list of dictionaries, where each dictionary represents a movie with attributes like position, name, release year, rating, and URL.

## Usage

To use this script:

1. Clone the repository or download the `imdb_scraper.py` file.

2. Make sure you have Python installed on your system.

3. Install the required libraries using pip:

```
pip install requests beautifulsoup4
```
   
5. Run the script:
```
python imdb_scraper.py
```


5. The script will print the scraped data or store it in a variable for further processing.

## Example Output

Here is an example of the data structure returned by the script:

```python
[
 {
     'position': 1,
     'name': 'Nayakan',
     'years': 1987,
     'rating': 8.5,
     'url': 'https://www.imdb.com/title/tt0093603/'
 },
 {
     'position': 2,
     'name': 'Anbe Sivam',
     'years': 2003,
     'rating': 8.5,
     'url': 'https://www.imdb.com/title/tt0367495/'
 },
]

```

## Contributing

Contributions are welcome! If you find any issues or want to add improvements, feel free to fork the repository, make your changes, and submit a pull request.

