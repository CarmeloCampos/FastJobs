from random import randint
from time import sleep
from urllib.parse import urlparse, parse_qs, unquote

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def run(token, session, header):
    payload = {'challengeToken': token}
    reqcaptcha = session.post("https://flex-capacity-na.amazon.com/ValidateChallenge", headers=header, json=payload)
    print(payload, reqcaptcha.status_code, reqcaptcha.text)
    if reqcaptcha.status_code == 200:
        print('Captcha Solved')
    else:
        print('Captcha not solved')


options = webdriver.ChromeOptions()
options.add_extension("Captcha-Solver-Auto-captcha-solving-service.crx")


class Solver(object):
    def __init__(self, user_agent):
        options.add_argument("--user-agent=" + user_agent)
        self.options = options
        self.driver: WebDriver = None
        self.open_new_driver_session()

    def open_new_driver_session(self):
        try:
            self.driver = webdriver.Remote(command_executor="http://192.168.50.3:4444/wd/hub", options=self.options)
        except WebDriverException as e:
            print(f"Error opening a new driver session: {e}")

    def is_driver_alive(self) -> bool:
        try:
            _ = self.driver.title
            return True
        except WebDriverException:
            return False

    def ensure_driver_is_alive(self):
        if self.driver is None or not self.is_driver_alive():
            print("Driver not available, opening a new session.")
            self.open_new_driver_session()

    def prepare(self):
        self.ensure_driver_is_alive()
        self.driver.get('chrome-extension://pgojnojmmhpofjgdmaebadhbocahppod/www/index.html#/popup')

        wait = WebDriverWait(self.driver, 10)
        input_api_key = wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'q-placeholder')))

        input_api_key.click()
        input_api_key.send_keys('CAP-230757974B6E422FAECA15002B49D7B1')
        sleep(1)
        button_save = self.driver.find_element(By.CLASS_NAME, 'text-balance')
        button_save.click()
        sleep(1)

    def intent_solve(self, url_captcha):
        self.ensure_driver_is_alive()
        print("Solving captcha")
        self.driver.get(url_captcha)

        initial_sleep_time = randint(8, 17)
        sleep(initial_sleep_time)

        while True:
            if 'uniqueValidationId' in self.driver.current_url:
                print("Captcha solved")
                break

            if self.driver.current_url != url_captcha:
                print("URL changed", url_captcha, self.driver.current_url)
                break

            sleep(1)

        return True

    def solve(self, url_captcha):
        self.ensure_driver_is_alive()
        if self.intent_solve(url_captcha):
            parsed_url = urlparse(self.driver.current_url)
            query_params = parse_qs(parsed_url.query)
            session_token = query_params['sessionToken'][0]
            return unquote(session_token)
