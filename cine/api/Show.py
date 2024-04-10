from dateutil import parser

class Show:
    def __init__(self, json_object):
        self._id = json_object['id']
        self._film = json_object['film']
        self._theater = json_object['theater']
        self._startDate = parser.isoparse(json_object['startDate']) if json_object['startDate'] != None else None
        self._endDate = parser.isoparse(json_object['endDate']) if json_object['endDate'] != None else None
        self._subtitles = json_object['subtitles']
        self._ticketingUrl = json_object['ticketingUrl']
        self._specials = json_object['specials']
        self._customSpecials = json_object['customSpecials']

    def __str__(self):
        return f"Show {self._id} - {self._film['title']} at {self._theater['name']} on {self._startDate}"