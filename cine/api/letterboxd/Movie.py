import re
from bs4 import BeautifulSoup
import requests

match_tmdb = re.compile(r"^https?://www.themoviedb.org")

class Movie:
    def __init__(self) -> None:
        self._title = None
        self._tmdb_id = None

    def loadFromInternet(self, movie):
        movie_url = "https://letterboxd.com/film/%s/" % movie.div.attrs["data-film-slug"]
        movie_page = requests.get(movie_url)
        soup = BeautifulSoup(movie_page.text, "html.parser")

        try:
            self._title = movie.div.attrs["data-film-slug"]
            movie_link = soup.find("a", attrs={"href": match_tmdb}).attrs["href"]
            self._tmdb_id = movie_link.split("/")[-2]
        
        except Exception:
            print("Parsing failed")
        
        return self
    
    def set(self, title: str, tmdb_id) -> None:
        self._title = title
        self._tmdb_id = tmdb_id
        return self
    
    def __str__(self):
        return f"{self._title} with TMDB ID {self._tmdb_id}"
    
    def getTMDBID(self) -> str:
        return self._tmdb_id
    
    def getTitle(self) -> str:
        return self._title
    
    def __eq__(self, other) -> bool:
        return self._tmdb_id == other.getTMDBID()