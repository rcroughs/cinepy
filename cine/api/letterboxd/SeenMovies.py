from bs4 import BeautifulSoup
from tqdm import tqdm
from .Movie import Movie
import requests
import os

seen_movies_pre = ".sm_"

class SeenMovies:
    def __init__(self, account_name, minimal=False) -> None:
        self._account_name = account_name
        self._minimal = minimal
        self._seen_movies = self.fetchSeenMovies()

    def fetchSeenMovies(self) -> list[list[str]]:
        self._seen_movies = []
        seen_movies_url = f"https://letterboxd.com/{self._account_name}/films/"
        response = requests.get(seen_movies_url)
        soup = BeautifulSoup(response.text, "html.parser")
        # To find the total number of movies, you have that information in this <a href="/korzie/films/" class="tooltip" data-original-title="317&nbsp;films">Watched</a>
        movies = soup.find("a", attrs={"class": "tooltip", "href": f"/{self._account_name}/films/"})
        if len(movies) > 0:
            total_movies = int(movies.get("title").split()[0])
            
        self._cached_seen_movies = []
        self.loadFromFile(seen_movies_pre + self._account_name, self._cached_seen_movies)
        
        number_of_pages = int(soup.find_all("li", attrs={"class": "paginate-page"})[-1].text)
        with tqdm(total=total_movies, desc=f"🚀 Fetching seen movies for {self._account_name}", disable=(True if self._minimal else False)) as pbar:
            for page in range(1, number_of_pages + 1):
                if page > 1:
                    response = requests.get(f"{seen_movies_url}page/{page}/")
                    soup = BeautifulSoup(response.text, "html.parser")
                
                ul = soup.find("ul", attrs={"class": "poster-list"})
                li = ul.find_all("li")
                for movie in li:
                    found_in_cache = False
                    for sm_movie in self._cached_seen_movies:
                        if sm_movie.getTitle() == movie.div.attrs["data-film-slug"]:
                            found_in_cache = True
                            self._seen_movies.append(sm_movie)
                            pbar.update(1)
                            break
                    if not found_in_cache:
                        self._seen_movies.append(Movie().loadFromInternet(movie))
                        pbar.update(1)
                    
        self.saveSeenMovies(seen_movies_pre + self._account_name)
        return self._seen_movies
    
    def loadFromFile(self, filename: str, list) -> None:
        if os.path.isfile(filename):
            with open(filename, "r") as file:
                for line in file:
                    movie = line.strip()
                    movie_infos = movie.split(",")
                    list.append(Movie().set(movie_infos[0], movie_infos[1]))

    def getSeenMoviesSize(self) -> int:
        return len(self._seen_movies) - 1
    
    def saveSeenMovies(self, filename: str) -> None:
        with open(filename, "w") as file:
            for movie in self._seen_movies:
                file.write(f"{movie.getTitle()},{movie.getTMDBID()}\n")
    
    def getSeenMovies(self) -> list[Movie]:
        return self._seen_movies
    
    def getSeenMovie(self, index: int) -> Movie:
        return self._seen_movies[index]
    
    def getSeenMovieByTMDBID(self, tmdb_id: str) -> Movie:
        for movie in self._seen_movies:
            if movie.getTMDBID() == tmdb_id:
                return movie
        return None