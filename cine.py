#!/usr/bin/python3

from cine.api.letterboxd.WatchList import WatchList
from cine.api.letterboxd.SeenMovies import SeenMovies
from cine.api.Showtimes import Showtimes
from datetime import datetime, timedelta
from cine.api.Show import Show
from cine.api.Theaters import Theaters
from math import log
import argparse
from cine.display import display_showtimes, display_showtimes_with_account



def main(args) -> int:
    current_date = datetime.now() + timedelta(days=args.days)
    # if no days are specified, we want to display the showtimes for the current day
    if args.days != 0:
        current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
    next_day = current_date + timedelta(days=args.period)
    next_day = next_day.replace(hour=0, minute=0, second=0, microsecond=0)
    f_theaters = []
    theaters = Theaters(args.cities, minimal=args.minimal)
    if args.theater is not None:
        for theater in theaters.getTheaters():
            if theater.getSlug() in args.theater:
                f_theaters.append(theater)
    showtimes = Showtimes(args.cities, dateBegin=current_date, dateEnd=next_day, theaters=f_theaters, minimal=args.minimal)
    if args.account is not None:
        watchlist = WatchList(args.account, minimal=args.minimal)
        seen_movies = SeenMovies(args.account, minimal=args.minimal)
        display_showtimes_with_account(showtimes, watchlist, theaters, seen_movies, args.limit, args.ignore, args.minimal)
    else:
        display_showtimes(showtimes, theaters, args.limit, args.minimal)
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
    parser.add_argument("-i", "--ignore", help="Ignore the movies that you have already seen", action="store_true", required=False)
    parser.add_argument("-f", "--full", help="Display full showtimes", action="store_true", required=False)
    parser.add_argument("-m", "--minimal", help="Minimal Display (for fuzzy finding for example)", action="store_true", required=False)
    args = parser.parse_args()
    if args.full:
        args.period = 8
    sys.exit(main(args))