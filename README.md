# Cinepy
`cine.py` is a python script that connects the [Cineville](https://cinevillepass.be/) API to different services such as Letterboxd, Google Calendar, etc.

## Configuration
To make the program run, you have to get a [TMDB](https://www.themoviedb.org/) key in a `.env` file.

## Usage
```
usage: cine.py [-h] [-a ACCOUNT] [-d DAYS] [-p PERIOD] [-c CITIES [CITIES ...]] [-l LIMIT] [-t THEATER [THEATER ...]]

Display showtimes of Cinevillepass

options:
  -h, --help            show this help message and exit
  -a ACCOUNT, --account ACCOUNT
                        Letterboxd account name
  -d DAYS, --days DAYS  Days offset for the query
  -p PERIOD, --period PERIOD
                        Period of time to query in days
  -c CITIES [CITIES ...], --cities CITIES [CITIES ...]
                        Cities to query
  -l LIMIT, --limit LIMIT
                        Limit of showtimes to fetch
  -t THEATER [THEATER ...], --theater THEATER [THEATER ...]
                        Theater to query
```

### Dependencies
All the dependencies are shown in the file `requirement.txt`.

### Greetings
Some of the code inside this project is based on other projects:
- [janw/letterboxd-rss](https://github.com/janw/letterboxd-rss)