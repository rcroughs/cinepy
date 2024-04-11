#!/usr/bin/python3

from cine.api.letterboxd.WatchList import WatchList
from cine.api.Showtimes import Showtimes
from datetime import datetime, timedelta
import cine.colors as colors
import argparse

def display_showtimes_with_wathlist(showtimes, watchlist):
    counter = 1
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

def display_showtimes(showtimes):
    counter = 1
    for showtime in showtimes.getShowtimes():
        print(f"({counter}) {showtime.getTitle()} at {showtime.getTheater()} on {showtime.getStartDate()}")
        counter += 1

def main(args) -> int:
    current_date = datetime.now() + timedelta(days=args.days)
    # if no days are specified, we want to display the showtimes for the current day
    if args.days is not None:
        current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
    next_day = current_date + timedelta(days=1)
    next_day = next_day.replace(hour=0, minute=0, second=0, microsecond=0)
    showtimes = Showtimes(args.cities, dateBegin=current_date, dateEnd=next_day, limit=args.limit)
    if args.account is not None:
        watchlist = WatchList(args.account)
        display_showtimes_with_wathlist(showtimes, watchlist)
    else:
        display_showtimes(showtimes)
    return 0

if __name__ == "__main__":
    import sys
    parser = argparse.ArgumentParser(prog="cine.py", description="Display showtimes of Cinevillepass")
    parser.add_argument("-a", "--account", help="Letterboxd account name", required=False)
    parser.add_argument("-d", "--days", help="Days offset for the query", type=int, default=0, required=False)
    parser.add_argument('-c', '--cities', nargs='+', help="Cities to query", default=[], required=False)
    parser.add_argument("-l", "--limit", help="Limit of showtimes to fetch", type=int, default=50, required=False)
    args = parser.parse_args()
    sys.exit(main(args))