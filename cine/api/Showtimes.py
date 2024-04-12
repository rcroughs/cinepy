import requests
from datetime import datetime
import time
from .Show import Show
from .k_cities import k_cities
from .Theater import Theater

class Showtimes:
    def __init__(self, cities: list[str], dateBegin: datetime, dateEnd: datetime, theaters: list[Theater], limit=0) -> None:
        self._url = "https://cinevillepass.be/api/graphql"
        self._cities = cities
        self._dateBegin = dateBegin
        self._dateEnd = dateEnd
        self._limit = limit
        self._theaters = theaters
        self._showtimes = self.fetchShowtimes()

    def fetchShowtimes(self) -> list[Show]:
        print(f"🚀 Fetching showtimes from {self._dateBegin} to {self._dateEnd}")
        r = requests.post(url = self._url, json = {"operationName": "showtimes", "query": "query showtimes(  $filters: ShowtimesFilters  $collections: [CollectionFilter!]  $page: CursorPagination  $sort: ShowtimesSort  $locale: String) {  showtimes(    filters: $filters    collections: $collections    page: $page    sort: $sort    locale: $locale  ) {    totalCount    data {      startDate      endDate      film {        id        slug        title        releaseYear      }      theater {        id      }    }    count  }}", 
                                                                                "variables" : {
                                                                                    "collections": [{"collectionGroupId": "cities", "collectionId": city, "id": str(k_cities[city])} for city in self._cities],
                                                                                    "filters": {
                                                                                        "startDate": {
                                                                                            "gte": self.local2utc(self._dateBegin).isoformat(),
                                                                                            "lte": self.local2utc(self._dateEnd).isoformat()
                                                                                        },
                                                                                        "venueId": {"in": [theater.getID() for theater in self._theaters]}
                                                                                    },
                                                                                    "page": {
                                                                                        "limit": self._limit if self._limit > 0 else 1000
                                                                                        }
                                                                                    }
                                                                                })
        if r.status_code != 200:
            raise Exception(f"Error {r.status_code}: {r.text}")
        json = r.json()
        showList = []
        for show in json['data']['showtimes']['data']:
            showList.append(Show(show))
        return showList
    
    def getShowtimes(self) -> list[Show]:
        return self._showtimes

    def local2utc(self, local: datetime) -> datetime:
        epoch = time.mktime(local.timetuple())
        offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
        return local - offset