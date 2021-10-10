import requests


def make_request(endpoint):
    """
    Make a request to the given URL and return the response.
    """
    return requests.get(
        f"https://api.audioboom.com{endpoint}",
        # The API needs version specifying
        headers={'Accept': 'application/json; version=1'}
    ).json()["body"]


def make_slug(title):
    long = ''.join([
        s if s in '0123456789-abcdefghijklmnopqrstuvwxyz'
        else '-'
        for s in title.lower().strip()
        ])
    xs = [x for x in long.split("-") if not short_word(x)]

    return "-".join(xs)


def short_word(w):
    return w in [
        "", "the", "a"
    ]
