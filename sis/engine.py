from threading import Thread

from sis.bot import flex

Finder = Thread(target=flex.run, args=())


def reload_finder():
    global Finder
    Finder = Thread(target=flex.run, args=())


def get_fresh_finder():
    global Finder
    return Finder
