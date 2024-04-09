from json import load

from sis.config import configFile

langFile = load(open('langs/{}.json'.format(configFile['lang']), encoding='utf-8'))
