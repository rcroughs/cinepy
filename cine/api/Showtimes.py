import requests
from .Show import Show
from .k_cities import k_cities

class Showtimes:
    def __init__(self, url: str, cities: list[str], dateBegin: str, dateEnd: str, limit: int) -> None:
        self._url = url
        self._cities = cities
        self._dateBegin = dateBegin
        self._dateEnd = dateEnd
        self._limit = limit

    def getShowtimes(self) -> list[Show]:
        r = requests.post(url = self._url, json = {"operationName": "showtimes", "query": "query showtimes($filters: ShowtimesFilters, $collections: [CollectionFilter!], $page: CursorPagination, $sort: ShowtimesSort, $locale: String) {  showtimes(    filters: $filters    collections: $collections    page: $page    sort: $sort    locale: $locale  ) {    count    totalCount    data {      ...showtime      __typename    }    ...pageInfo    __typename  }}fragment asset on Asset {  url  mime  alternativeText  __typename}fragment filmHighlight on FilmHighlight {  type  author  endDate  startDate  description  active  __typename}fragment film on Film {  id  slug  title  cover {    ...asset    __typename  }  poster {    ...asset    __typename  }  trailer {    ...asset    __typename  }  cast  duration  directors  releaseYear  spokenLanguages  contentRatingMinimumAge  premiereDate  highlights {    ...filmHighlight    __typename  }  shortDescription  description  editorsNote  __typename}fragment address on Address {  street  houseNumber  postalCode  city  country  __typename}fragment theater on Theater {  id  slug  name  address {    ...address    __typename  }  cover {    ...asset    __typename  }  website  shortDescription  intro  description  ticketInfo  __typename}fragment showtime on Showtime {  id  film {    ...film    __typename  }  theater {    ...theater    __typename  }  startDate  endDate  subtitles  ticketingUrl  specials  customSpecials  __typename}fragment pageInfo on Response {  count  totalCount  previous  next  __typename}", 
                                                                                "variables" : {
                                                                                    "collections": [{"collectionGroupId": "cities", "collectionId": city, "id": str(k_cities[city])} for city in self._cities],
                                                                                    "filters": {
                                                                                        "startDate": {
                                                                                            "gte": self._dateBegin,
                                                                                            "lte": self._dateEnd
                                                                                        }
                                                                                    },
                                                                                    "page": {
                                                                                        "limit": self._limit
                                                                                        },
                                                                                    }
                                                                                })
        json = r.json()
        showList = []
        if 'errors' in json:
            print(json['errors'])
            return showList
        
        for show in json['data']['showtimes']['data']:
            showList.append(Show(show))
        return showList