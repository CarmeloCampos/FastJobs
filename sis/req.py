from requests import post


def req_solver(url_captcha):
    try:
        uwu_sol = post("http://apijobs:5000/solve-captcha", json={"url": url_captcha}).json()
        return uwu_sol.get("session_token")
    except Exception as e:
        print("Error solving captcha", e)
        return req_solver(url_captcha)
