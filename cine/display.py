from .api.Show import Show
import cine.colors as colors

def href(url: str, text: str) -> str:
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

def println(found_in_watchlist: bool, seen: bool, counter: int, showtime: Show, title_width: int, theater_width: int, date_width: int, length, theaters, minimal: bool) -> bool:
    line = "⭐" if found_in_watchlist else "  "
    counter_string = f"({counter:0{len(str(length))}d}) "
    text_color = ""
    if found_in_watchlist and not minimal:
        text_color = colors.YELLOW
    elif seen and not minimal:
        text_color = colors.DARK_GRAY

    if minimal:
        title = showtime.getTitle() + " " * (title_width - len(showtime.getTitle()))
    else:
        title = (text_color) + (href(f"https://www.letterboxd.com/tmdb/{showtime.getTMDBID()}", showtime.getTitle()) if (showtime.getTMDBID() != None) else showtime.getTitle()) + " " * (title_width - len(showtime.getTitle())) + colors.RESET
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
    if minimal:
        print(title + theater + date)
    else:
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

def display_showtimes_with_account(showtimes, watchlist, theaters, seen_movies, limit: int, ignore: bool, minimal: bool):
    counter = 1
    max_title_width, max_theater_width, max_date_width = getWidths(showtimes, theaters)
    for showtime in showtimes.getShowtimes():
        if limit is not None and counter >= limit:
            break
        found_in_watchlist = False
        found_in_seen_movies = False
        for movie in watchlist.getWatchList():
            if movie.getTMDBID() is not None and showtime.getTMDBID() is not None:
                if int(showtime.getTMDBID()) == int(movie.getTMDBID()):
                    found_in_watchlist = True
        for movie in seen_movies.getSeenMovies():
            if movie.getTMDBID() is not None and showtime.getTMDBID() is not None:
                if int(showtime.getTMDBID()) == int(movie.getTMDBID()):
                    found_in_seen_movies = True
        if not (found_in_seen_movies and ignore) and println(found_in_watchlist, found_in_seen_movies, counter, showtime, max_title_width + 7, max_theater_width + 7, max_date_width, len(showtimes.getShowtimes()), theaters, minimal):
            counter += 1

def display_showtimes(showtimes, theaters, limit: int, minimal: bool):
    counter = 1
    max_title_width, max_theater_width, max_date_width = getWidths(showtimes, theaters)
    for showtime in showtimes.getShowtimes():
        if limit is not None and counter >= limit:
            break
        if println(False, False, counter, showtime, max_title_width + 7, max_theater_width + 7, max_date_width, len(showtimes.getShowtimes()), theaters, minimal):
            counter += 1
