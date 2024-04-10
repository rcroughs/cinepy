#!/usr/bin/python3
import sys
sys.path.append('..')
from cine.api.Showtimes import Showtimes

def test_Showtimes():
    showtimes = Showtimes("https://cinevillepass.be/api/graphql", ["brussels"], "2024-04-10T15:45:00.000Z", "2024-04-11T02:00:00.000Z", 20)
    shows = showtimes.getShowtimes()
    for show in shows:
        print(show)

test_Showtimes()