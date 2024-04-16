from random import randint
from time import sleep
from urllib.parse import urlparse, parse_qs, unquote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Solver(object):
    def __init__(self, header):
        options = webdriver.ChromeOptions()
        options.add_extension("Captcha-Solver-Auto-captcha-solving-service.crx")
        options.add_argument(f"--user-agent={header}")
        self.options = options
        self.driver = None

    def set(self):
        if self.driver is None:
            self.driver = webdriver.Remote(command_executor="http://192.168.50.3:4444/wd/hub", options=self.options)

    def prepare(self):
        self.driver.get('chrome-extension://pgojnojmmhpofjgdmaebadhbocahppod/www/index.html#/popup')

        wait = WebDriverWait(self.driver, 10)
        input_api_key = wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'q-placeholder')))

        input_api_key.click()
        input_api_key.send_keys('CAP-230757974B6E422FAECA15002B49D7B1')
        sleep(1)
        button_save = self.driver.find_element(By.CLASS_NAME, 'text-balance')
        button_save.click()
        sleep(1)
        self.driver.save_screenshot('json/captcha.png')

    def solve(self, header, session):
        sleep(randint(5, 7))
        self.driver.get('https://www.amazon.com/aaut/verify/flex-offers/challenge?challengeType=ARKOSE_LEVEL_2'
                        '&returnTo=https://www.amazon.com&headerFooter=false')
        self.driver.save_screenshot('json/amazon.png')
        sleep(randint(17, 37))
        self.driver.save_screenshot('json/amazon2.png')
        parsed_url = urlparse(self.driver.current_url)
        query_params = parse_qs(parsed_url.query)
        session_token = query_params.get('sessionToken', [None])[0]
        print(session_token)
        decoded_session_token = unquote(session_token)

        payload = {'challengeToken': decoded_session_token}
        reqcaptcha = session.post("https://flex-capacity-na.amazon.com/ValidateChallenge", headers=header, json=payload)
        print(reqcaptcha.status_code, reqcaptcha.text)
        if reqcaptcha.status_code == 200:
            print('Captcha Solved')
        else:
            print('Captcha not solved')
