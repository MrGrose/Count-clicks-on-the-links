from os import getenv
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def shorten_link(token: str, url: str) -> dict[str]:
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
    data = response.json()
    return data['response']


def count_clicks(token: str, link: str) -> dict[str]:
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
    data = response.json()
    return data['response']


def is_shorten_link(token: str, url: str) -> bool:
    method = 'utils.getShortLink'
    url_template = f'https://api.vk.com/method/{method}'
    version = '5.199'
    params = {
        'access_token': token,
        'v': version,
        'url': url,
    }
    response = requests.get(url_template, params=params)
    response.raise_for_status()
    data = response.json()
    return True if 'response' not in data else False


def main() -> None:
    load_dotenv()
    token = getenv('API_VK')
    user_input = input('Enter the link: ')
    try:
        check_link = is_shorten_link(token, user_input)
        query = count_clicks(token, user_input) if check_link else shorten_link(token, user_input)
        if query.get('short_url'):
            print(f'Short link: {query.get('short_url')}')
        else:
            for key in query['stats']:
                print(f'Clicks: {key['views']}')
    except (requests.exceptions.HTTPError, ValueError, KeyError) as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    main()
