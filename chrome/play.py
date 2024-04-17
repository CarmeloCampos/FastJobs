import json
from os import path
from time import sleep
from urllib.parse import urlparse, parse_qs, unquote

from playwright.sync_api import sync_playwright

from lib import FlexUnlimited

token_nice = None


def update_token(res):
    if 'sessionToken' in res.url:
        global token_nice
        parsed_url = urlparse(res.url)
        query_params = parse_qs(parsed_url.query)
        print('query_params', query_params)
        decoded_session_token = unquote(query_params['sessionToken'][0])
        token_nice = decoded_session_token


def get_token():
    global token_nice
    return token_nice


def solve(father: FlexUnlimited):
    global token_nice
    with sync_playwright() as playwright:
        path_extension = path.join(path.dirname(__file__), 'capsolver')
        data_user = path.join(path.dirname(__file__), 'data_user')
        context = playwright.chromium.launch_persistent_context(args=[
            '--disable-extensions-except=' + path_extension,
            '--load-extension=' + path_extension
        ], headless=False, user_data_dir=data_user, user_agent=father.allHeaders.get('AmazonApiRequest')['User-Agent'])
        page = context.new_page()
        page.goto('chrome-extension://kiklbdccfdijffoghmfgdpeejdgdeoab/www/index.html#/popup')
        sleep(2)
        input_api_key = page.query_selector('.q-placeholder')
        input_api_key.click()
        input_api_key.fill('CAP-230757974B6E422FAECA15002B49D7B1')
        sleep(1)

        button_save = page.query_selector('.text-balance')
        button_save.click()
        sleep(1)
        url_solve = ('https://www.amazon.com/aaut/verify/flex-offers/challenge?challengeType=ARKOSE_LEVEL_2&'
                     'returnTo=https://www.amazon.com&headerFooter=false')
        page.goto(url_solve)
        page.on('response', update_token)
        sleep(30)
        payload = json.dumps({'challengeToken': get_token()})
        reqcaptcha = father.session.post("https://flex-capacity-na.amazon.com/ValidateChallenge",
                                         headers=father.sign_validity_headers(), data=payload)
        print(payload, reqcaptcha.status_code, reqcaptcha.text)
        if reqcaptcha.status_code == 200:
            print('Captcha Solved')
        else:
            print('Captcha not solved')
