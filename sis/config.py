from json import load

nameFile = 'json/config.json'
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
