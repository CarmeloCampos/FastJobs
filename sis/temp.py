Finding = False


def update_finding(status: bool):
    global Finding
    Finding = status


def get_finder():
    global Finding
    return Finding
