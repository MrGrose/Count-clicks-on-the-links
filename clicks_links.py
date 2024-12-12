from os import getenv
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def shorten_link(token: str, url: str) -> str:
    method = 'utils.getShortLink'
    url_template = f'https://api.vk.com/method/{method}'
    version = '5.199'
    param = {
        'access_token': token,
        'v': version,
        'url': url,
        }
    response = requests.get(url_template, params=param)
    response.raise_for_status()
    short_url = response.json()
    return short_url['response']['short_url']


def count_clicks(token: str, link: str) -> int:
    parsed = urlparse(link)
    method = 'utils.getLinkStats'
    version = '5.199'
    url_tempale = f'https://api.vk.com/method/{method}'
    param = {
        'access_token': token,
        'v': version,
        'key': parsed.path[1:],
        'interval': 'forever',
        }
    response = requests.get(url_tempale, params=param)
    response.raise_for_status()
    views = response.json()
    return views['response']['stats'][0]['views']


def is_shorten_link(token: str, url: str) -> bool:
    method = 'utils.getShortLink'
    url_template = f'https://api.vk.com/method/{method}'
    version = '5.199'
    param = {
        'access_token': token,
        'v': version,
        'url': url,
    }
    response = requests.get(url_template, params=param)
    response.raise_for_status()
    short_link = response.json()
    return 'response' not in short_link


def main() -> None:
    load_dotenv()
    token = getenv('VK_TOKEN')
    user_input = input('Enter the link: ')
    try:
        check_link = is_shorten_link(token, user_input)
        query = count_clicks(token, user_input) if check_link else shorten_link(token, user_input)
        print(query)
    except (requests.exceptions.HTTPError, ValueError, KeyError) as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    main()
