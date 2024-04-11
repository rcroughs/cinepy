#!/usr/bin/python3

from cine.api.letterboxd.WatchList import WatchList
from cine.api.Showtimes import Showtimes
from datetime import datetime, timedelta
from cine.api.Show import Show
from math import log
import cine.colors as colors
import argparse


def println(found_in_watchlist: bool, counter: int, showtime: Show, title_width: int, theater_width: int, date_width: int, length):
    line = "⭐" if found_in_watchlist else "  "
    counter_string = f"({counter:0{len(str(length))}d}) "
    title = (colors.YELLOW if found_in_watchlist else "") + showtime.getTitle().ljust(title_width) + colors.RESET
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
        display_showtimes_with_watchlist(showtimes, watchlist)
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