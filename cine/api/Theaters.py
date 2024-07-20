import requests
from .k_cities import k_cities
from .Theater import Theater


class Theaters:
    def __init__(self, cities: list[str], minimal=False) -> None:
        self._url = "https://cinevillepass.be/api/graphql"
        self._cities = cities
        self._minimal = minimal
        self._theaters = self.fetchTheaters()

    def fetchTheaters(self) -> list[Theater]:
        print(f"🚀 Fetching theaters") if not self._minimal else None
        r = requests.post(
            url=self._url,
            json={
                "operationName": "theaters",
                "query": "query theaters($filters: TheatersFilters, $collections: [CollectionFilter!], $page: CursorPagination, $sort: TheatersSort, $locale: String) {  theaters(    filters: $filters    collections: $collections    page: $page    sort: $sort    locale: $locale  ) {    data {      ...theater      __typename    }    ...pageInfo    __typename  }}fragment address on Address {  street  houseNumber  postalCode  city  country  __typename}fragment asset on Asset {  url  mime  alternativeText  __typename}fragment theater on Theater {  id  slug  name  address {    ...address    __typename  }  cover {    ...asset    __typename  }  website  shortDescription  intro  description  ticketInfo  __typename}fragment pageInfo on ListResponse {  count  totalCount  previous  next  __typename}",
                "variables": {
                    "collections": [
                        {
                            "collectionGroupId": "cities",
                            "collectionId": city,
                            "id": str(k_cities[city]),
                        }
                        for city in self._cities
                    ]
                },
            },
        )
        if r.status_code != 200:
            raise Exception(f"Error {r.status_code}: {r.text}")
        json = r.json()
        print(json)
        theaterList = []
        for theater in json["data"]["theaters"]["data"]:
            theaterList.append(Theater(theater))
        return theaterList

    def getTheaters(self) -> list[Theater]:
        return self._theaters

    def getTheater(self, id: str) -> Theater:
        for theater in self._theaters:
            if theater.getID() == id:
                return theater
        return None
