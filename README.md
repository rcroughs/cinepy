# Cinepy
`cine.py` is a python script that connects the [Cineville](https://cinevillepass.be/) API to different services such as Letterboxd, Google Calendar, etc.

## Usage
```
usage: cine.py [-h] [-a ACCOUNT] [-d DAYS] [-c CITIES [CITIES ...]]

Display showtimes of Cinevillepass

options:
  -h, --help            show this help message and exit
  -a ACCOUNT, --account ACCOUNT
                        Letterboxd account name
  -d DAYS, --days DAYS  Days offset for the query
  -c CITIES [CITIES ...], --cities CITIES [CITIES ...]
                        Cities to query
```

### Dependencies
All the dependencies are shown in the file `requirement.txt`.

### Greetings
Some of the code inside this project is based on other projects:
- [janw/letterboxd-rss](https://github.com/janw/letterboxd-rss)