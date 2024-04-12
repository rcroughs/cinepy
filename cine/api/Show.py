from dateutil import parser
from datetime import datetime
import time
import requests
import webbrowser

from dotenv import load_dotenv
import os

load_dotenv()

class Show:
    def __init__(self, json_object):
        self._slug = json_object['film']['slug']
        self._title = json_object['film']['title']
        self._releaseYear = json_object['film']['releaseYear']
        self._theater_id = json_object['theater']['id']
        self._startDate = self.utc2local(parser.isoparse(json_object['startDate'])) if json_object['startDate'] != None else None
        self._endDate = self.utc2local(parser.isoparse(json_object['endDate'])) if json_object['endDate'] != None else None
        self.fetchTMDBID()

    def utc2local(self, utc):
        epoch = time.mktime(utc.timetuple())
        offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
        return utc + offset
    

    def fetchTMDBID(self) -> str:
        url = f"https://api.themoviedb.org/3/search/movie?query={self._slug}&include_adult=false&year={self._releaseYear}"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + os.getenv("TMDB_API_KEY")
        }
        response = requests.get(url, headers=headers)
        if len(response.json()['results']) == 0:
            self._tmdb_id = None
        else:
            self._tmdb_id = response.json()['results'][0]['id']


    def getTMDBID(self) -> str:
        if not hasattr(self, '_tmdb_id'):
            self.fetchTMDBID()
        return self._tmdb_id
    
    def getTitle(self) -> str:
        return self._title
    
    def getStartDate(self) -> datetime:
        return self._startDate
    
    def getEndDate(self) -> datetime:
        return self._endDate

    def getTheaterId(self) -> str:
        return self._theater_id
    
    def getSlug(self) -> str:
        return self._slug

    def __str__(self):
        return f"{self._film['title']} at {self._theater['name']} on {self._startDate}"

    def createGoogleCalendarEvent(self, theaterList) -> str:
        if self._endDate == None:
            return ""
        theater = theaterList.getTheater(self._theater_id)
        theaterStreet = theater.getAddress()['street']
        theaterHouseNumber = theater.getAddress()['houseNumber']
        theaterPostalCode = theater.getAddress()['postalCode']
        theaterCity = theater.getAddress()['city']
        return f"https://www.google.com/calendar/render?action=TEMPLATE&text={self._title}&dates={self._startDate.strftime('%Y%m%dT%H%M%S')}/{self._endDate.strftime('%Y%m%dT%H%M%S')}&location={theaterStreet+' '+ theaterHouseNumber +' '+ theaterPostalCode +' '+ theaterCity}"