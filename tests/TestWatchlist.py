#!/usr/bin/python3
import sys
sys.path.append('..')
from cine.api.letterboxd.WatchList import WatchList 

def test_WatchList():
    watchlist = WatchList("korzie")
    print(watchlist)
    print(watchlist.getWatchListSize())

test_WatchList()