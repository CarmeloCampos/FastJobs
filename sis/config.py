from json import load

configFile = load(open('json/config.json'))
allow_admins = [496499134, 5509305]


def readConfigFile():
    file = load(open('json/config.json'))
    return file


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
    nowFile = load(open('json/config.json'))
    return nowFile.get(key)
