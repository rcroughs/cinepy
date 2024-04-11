#!/usr/bin/python3

from cine.api.letterboxd.WatchList import WatchList
from cine.api.Showtimes import Showtimes
from datetime import datetime, timedelta
import cine.colors as colors
import argparse

def display_showtimes(showtimes, watchlist):
    counter = 0
    for showtime in showtimes.getShowtimes():
        found_in_watchlist = False
        for movie in watchlist.getWatchList():
            if movie.getTMDBID() is not None and showtime.getTMDBID() is not None:
                if int(showtime.getTMDBID()) == int(movie.getTMDBID()):
                    found_in_watchlist = True
        if found_in_watchlist:
            print(f"⭐({counter}){colors.YELLOW} {showtime.getTitle()} {colors.RESET} at {showtime.getTheater()} on {showtime.getStartDate()}")
        else:
            not_found = f"{colors.DARK_GRAY}?{colors.RESET}" if showtime.getTMDBID() is None else ""
            print(f"  ({counter}) {showtime.getTitle()} at {showtime.getTheater()} on {showtime.getStartDate()} {not_found}")
        counter += 1

def main(*args) -> int:
    parser = argparse.ArgumentParser(prog="cinepy", description="Display showtimes of Cinevillepass")
    parser.add_argument("-a", "--account", help="Letterboxd account name", required=False)
    parser.add_argument("-d", "--days", default=0, help="Days offset for the query", required=False)

    current_date = datetime.now()
    next_day = current_date + timedelta(days=1)
    next_day = next_day.replace(hour=0, minute=0, second=0, microsecond=0)
    showtimes = Showtimes(["brussels"], dateBegin=current_date, dateEnd=next_day, limit=50)
    watchlist = WatchList("korzie")
    display_showtimes(showtimes, watchlist)
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(*sys.argv[1:]))