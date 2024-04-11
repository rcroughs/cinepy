import os
import requests
from .Movie import Movie
from bs4 import BeautifulSoup

watchlist_file = ".wl"

class WatchList:
    def __init__(self, account_name: str) -> None:
        self._account_name = account_name
        self._watchlist = self.getWatchList()
        
    def getWatchList(self) -> list[list[str]]:
        self._watchlist = []
        watchlist_url = f"https://letterboxd.com/{self._account_name}/watchlist/"
        response = requests.get(watchlist_url)
        soup = BeautifulSoup(response.text, "html.parser")
        movies = soup.find("span", attrs={"class": "js-watchlist-count"})
        if len(movies) > 0:
            total_movies = int(movies.text.split()[0])
            print(f"Total movies in watchlist: {total_movies}")

        self._cached_watchlist = []
        self.loadFromFile(watchlist_file, self._cached_watchlist)
        
        number_of_pages = int(soup.find_all("li", attrs={"class": "paginate-page"})[-1].text)
        for page in range(1, number_of_pages):
            if page > 1:
                response = requests.get(f"{watchlist_url}page/{page}/")
                soup = BeautifulSoup(response.text, "html.parser")
            
            ul = soup.find("ul", attrs={"class": "poster-list"})
            li = ul.find_all("li")
            for movie in li:
                found_in_cache = False
                for wl_movie in self._cached_watchlist:
                    if wl_movie.getTitle() == movie.div.attrs["data-film-slug"]:
                        found_in_cache = True
                        self._watchlist.append(wl_movie)
                        break
                if not found_in_cache:
                    self._watchlist.append(Movie().loadFromInternet(movie))
                    print(f"Added {self._watchlist[-1]} to watchlist")
        self.saveWatchList(watchlist_file)
        return self._watchlist
    
    def loadFromFile(self, filename: str, list) -> None:
        if os.path.isfile(filename):
            with open(filename, "r") as file:
                for line in file:
                    movie = line.strip()
                    movie_infos = movie.split(",")
                    list.append(Movie().set(movie_infos[0], movie_infos[1]))

    def getWatchListSize(self) -> int:
        return len(self._watchlist) - 1
    
    def saveWatchList(self, watchlist_file: str) -> None:
        with open(watchlist_file, "w") as file:
            for movie in self._watchlist:
                file.write(f"{movie.getTitle()},{movie.getTMDBID()}\n")
    
    def __str__(self):
        return f"WatchList {self._account_name} with {self.getWatchListSize()} movies"
