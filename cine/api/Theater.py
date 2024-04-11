class Theater:
    def __init__(self, json_object: dict) -> None:
        self._id = json_object['id']
        self._slug = json_object['slug']
        self._name = json_object['name']
        self._address = json_object['address']
        self._cover = json_object['cover']
        self._website = json_object['website']
        self._shortDescription = json_object['shortDescription']
        self._intro = json_object['intro']
        self._description = json_object['description']
        self._ticketInfo = json_object['ticketInfo']
    
    def getID(self) -> str:
        return self._id
    
    def getSlug(self) -> str:
        return self._slug
    
    def getName(self) -> str:
        return self._name