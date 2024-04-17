import json
from urllib.parse import unquote, urlparse, parse_qs

from anticaptchaofficial.antigatetask import antigateTask


def solve_anti(headers, session):
    print("Trying bypass captcha.")

    solver = antigateTask()
    solver.set_verbose(1)
    solver.set_key("4b8b7171e3cacd8b6a273e6cbec432b1")
    solver.set_website_url(
        "https://www.amazon.com/aaut/verify/flex-offers/challenge?challengeType=ARKOSE_LEVEL_2&"
        "returnTo=https://www.amazon.com&headerFooter=false")
    solver.set_template_name("Amazon uniqueValidationId")
    solver.set_variables({})

    result = solver.solve_and_return_solution()
    if result != 0:

        parsed_url = urlparse(result["url"])
        query_params = parse_qs(parsed_url.query)
        decoded_session_token = unquote(query_params['sessionToken'][0])

        payload = json.dumps({'challengeToken': decoded_session_token})
        ValidateChallenge = session.post("https://flex-capacity-na.amazon.com/ValidateChallenge", headers=headers,
                                         data=payload)
        print(ValidateChallenge.status_code, ValidateChallenge.text)
        if ValidateChallenge.status_code == 200:
            print("Captcha passed!")
            solver.report_correct_recaptcha()
        else:
            print("Reporting incorrect captcha.")
            solver.report_incorrect_recaptcha()

    else:
        print(f"Task finished with error {solver.error_code}")
