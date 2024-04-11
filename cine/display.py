from .api.Show import Show
import cine.colors as colors

def href(url: str, text: str) -> str:
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

def println(found_in_watchlist: bool, counter: int, showtime: Show, title_width: int, theater_width: int, date_width: int, length):
    line = "⭐" if found_in_watchlist else "  "
    counter_string = f"({counter:0{len(str(length))}d}) "
    title = (colors.YELLOW if found_in_watchlist else "") + (href(f"https://www.letterboxd.com/tmdb/{showtime.getTMDBID()}", showtime.getTitle()) if (showtime.getTMDBID() != None) else showtime.getTitle()) + " " * (title_width - len(showtime.getTitle())) + colors.RESET
    theater = showtime.getTheater().ljust(theater_width)
    date = str(showtime.getStartDate()).ljust(date_width)
    not_found = f"{colors.DARK_GRAY}?{colors.RESET}" if showtime.getTMDBID() is None else ""
    print(line + counter_string + title + theater + date + not_found)

def getWidths(showtimes):
    max_title_width = 0
    max_theater_width = 0
    max_date_width = 0
    for showtime in showtimes.getShowtimes():
        max_title_width = max(max_title_width, len(showtime.getTitle()))
        max_theater_width = max(max_theater_width, len(showtime.getTheater()))
        max_date_width = max(max_date_width, len(str(showtime.getStartDate())))
    return max_title_width, max_theater_width, max_date_width

def display_showtimes_with_watchlist(showtimes, watchlist):
    counter = 1
    max_title_width, max_theater_width, max_date_width = getWidths(showtimes)
    for showtime in showtimes.getShowtimes():
        found_in_watchlist = False
        for movie in watchlist.getWatchList():
            if movie.getTMDBID() is not None and showtime.getTMDBID() is not None:
                if int(showtime.getTMDBID()) == int(movie.getTMDBID()):
                    found_in_watchlist = True
        println(found_in_watchlist, counter, showtime, max_title_width + 7, max_theater_width + 7, max_date_width, len(showtimes.getShowtimes()))
        counter += 1

def display_showtimes(showtimes):
    counter = 1
    max_title_width, max_theater_width, max_date_width = getWidths(showtimes)
    for showtime in showtimes.getShowtimes():
        println(False, counter, showtime, max_title_width + 7, max_theater_width + 7, max_date_width, showtimes.getShowtimes())
        counter += 1