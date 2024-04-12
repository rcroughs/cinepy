#!/usr/bin/python3

from cine.api.letterboxd.WatchList import WatchList
from cine.api.Showtimes import Showtimes
from datetime import datetime, timedelta
from cine.api.Show import Show
from cine.api.Theaters import Theaters
from math import log
import argparse
from cine.display import display_showtimes, display_showtimes_with_watchlist



def main(args) -> int:
    current_date = datetime.now() + timedelta(days=args.days)
    # if no days are specified, we want to display the showtimes for the current day
    if args.days != 0:
        current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
    next_day = current_date + timedelta(days=args.period)
    next_day = next_day.replace(hour=0, minute=0, second=0, microsecond=0)
    f_theaters = []
    theaters = Theaters(args.cities)
    if args.theater is not None:
        for theater in theaters.getTheaters():
            if theater.getSlug() in args.theater:
                f_theaters.append(theater)
    showtimes = Showtimes(args.cities, dateBegin=current_date, dateEnd=next_day, theaters=f_theaters)
    if args.account is not None:
        watchlist = WatchList(args.account)
        display_showtimes_with_watchlist(showtimes, watchlist, theaters)
    else:
        display_showtimes(showtimes, theaters)
    return 0

if __name__ == "__main__":
    import sys
    parser = argparse.ArgumentParser(prog="cine.py", description="Display showtimes of Cinevillepass")
    parser.add_argument("-a", "--account", help="Letterboxd account name", required=False)
    parser.add_argument("-d", "--days", help="Days offset for the query", type=int, default=0, required=False)
    parser.add_argument("-p", "--period", help="Period of time to query in days", type=int, default=1, required=False)
    parser.add_argument('-c', '--cities', nargs='+', help="Cities to query", default=[], required=False)
    parser.add_argument("-l", "--limit", help="Limit of showtimes to fetch", type=int, required=False)
    parser.add_argument("-t", "--theater", help="Theater to query", nargs='+', required=False)
    args = parser.parse_args()
    sys.exit(main(args))