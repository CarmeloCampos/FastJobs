from json import load
from os import environ

nameFile = 'json/{}.json'.format(environ.get('CONFIG', 'config'))
configFile = load(open(nameFile))

flex_data = {
    'waiting_login': False,
    'code_verifier': None,
    'ready_login': False
}


def set_flex_data(key, value):
    global flex_data
    flex_data[key] = value


def get_flex_data(key):
    return flex_data.get(key)


def get_now_data(key):
    nowFile = load(open(nameFile))
    return nowFile.get(key)


def get_one_offer():
    return load(open('json/offers.json'))[0]
