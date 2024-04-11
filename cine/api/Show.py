from dateutil import parser
from datetime import datetime
import time
import requests

from dotenv import load_dotenv
import os

load_dotenv()

class Show:
    def __init__(self, json_object):
        self._id = json_object['id']
        self._film = json_object['film']
        self._slug = json_object['film']['slug']
        self._title = json_object['film']['title']
        self._releaseYear = json_object['film']['releaseYear']
        self._theater = json_object['theater']
        self._startDate = self.utc2local(parser.isoparse(json_object['startDate'])) if json_object['startDate'] != None else None
        self._endDate = self.utc2local(parser.isoparse(json_object['endDate'])) if json_object['endDate'] != None else None
        self._subtitles = json_object['subtitles']
        self._ticketingUrl = json_object['ticketingUrl']
        self._specials = json_object['specials']
        self._customSpecials = json_object['customSpecials']
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

    def getTheater(self) -> dict:
        return self._theater["name"]

    def __str__(self):
        return f"Show {self._id} - {self._film['title']} at {self._theater['name']} on {self._startDate}"