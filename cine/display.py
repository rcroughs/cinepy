from .api.Show import Show
import cine.colors as colors

def href(url: str, text: str) -> str:
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

def println(found_in_watchlist: bool, counter: int, showtime: Show, title_width: int, theater_width: int, date_width: int, length, theaters) -> bool:
    line = "⭐" if found_in_watchlist else "  "
    counter_string = f"({counter:0{len(str(length))}d}) "
    title = (colors.YELLOW if found_in_watchlist else "") + (href(f"https://www.letterboxd.com/tmdb/{showtime.getTMDBID()}", showtime.getTitle()) if (showtime.getTMDBID() != None) else showtime.getTitle()) + " " * (title_width - len(showtime.getTitle())) + colors.RESET
    if theaters.getTheater(showtime.getTheaterId()) is not None:
        theater_name = theaters.getTheater(showtime.getTheaterId()).getName()
    else:
        # Sometimes the showtimes filter out showtimes that are not in the cities specified
        # Returning early here to avoid bad results
        return False
    theater = theater_name.ljust(theater_width)
    date = str(showtime.getStartDate()).ljust(date_width)
    calendar = href(showtime.createGoogleCalendarEvent(theaters), f"{colors.DARK_GRAY}📅{colors.RESET}")
    not_found = f"{colors.DARK_GRAY}?{colors.RESET}" if showtime.getTMDBID() is None else ""
    print(line + counter_string + title + theater + date + calendar +not_found)
    return True

def getWidths(showtimes, theaters):
    max_title_width = 0
    max_theater_width = 0
    max_date_width = 0
    for showtime in showtimes.getShowtimes():
        max_title_width = max(max_title_width, len(showtime.getTitle()))
        if theaters.getTheater(showtime.getTheaterId()) is not None:
            max_theater_width = max(max_theater_width, len(theaters.getTheater(showtime.getTheaterId()).getName()))
        max_date_width = max(max_date_width, len(str(showtime.getStartDate())))
    return max_title_width, max_theater_width, max_date_width

def display_showtimes_with_watchlist(showtimes, watchlist, theaters):
    counter = 1
    max_title_width, max_theater_width, max_date_width = getWidths(showtimes, theaters)
    for showtime in showtimes.getShowtimes():
        found_in_watchlist = False
        for movie in watchlist.getWatchList():
            if movie.getTMDBID() is not None and showtime.getTMDBID() is not None:
                if int(showtime.getTMDBID()) == int(movie.getTMDBID()):
                    found_in_watchlist = True
        if println(found_in_watchlist, counter, showtime, max_title_width + 7, max_theater_width + 7, max_date_width, len(showtimes.getShowtimes()), theaters):
            counter += 1

def display_showtimes(showtimes, theaters):
    counter = 1
    max_title_width, max_theater_width, max_date_width = getWidths(showtimes, theaters)
    for showtime in showtimes.getShowtimes():
        if println(False, counter, showtime, max_title_width + 7, max_theater_width + 7, max_date_width, len(showtimes.getShowtimes()), theaters):
            counter += 1