from requests import request


def short_url(url):
    response = request("POST", "https://api.tinyurl.com/create",
                       json={"url": url},
                       headers={"Content-Type": "application/json",
                                "Authorization": "Bearer tQu6Po46gmSZ32l1t56zmnr0YMxHA0B4psTkNI0jfzNB0VrybSyXmjxLv49T",
                                "Accept": "application/json"})
    tiny_url = response.json()
    return tiny_url["data"]['tiny_url']
