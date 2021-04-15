import time
import requests


def request_apache_log(base_url):
    try_connection = 3
    while try_connection:
        try:
            response = requests.get(base_url)
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
            try_connection -= 1
            time.sleep(2)
            continue
        else:
            print('====Success request get====')
            return response
    else:
        raise requests.exceptions.ConnectionError(
            f'Max retries exceeded with url: {base_url}')
