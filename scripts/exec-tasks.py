' python3 call_n_tasks.py '
import asyncio
import requests
from time import time
from datetime import datetime as dt
from contextlib import contextmanager
from aiohttp import ClientSession


@contextmanager
def timed():
    'Simple timer context manager, implemented using a generator function'
    start = time()
    print("Staring at {:%H:%M:%S}".format(dt.fromtimestamp(start)))

    yield

    end = time()
    print("Ending at {:%H:%M:%S} (total: {:.2f} seconds)".format(
        dt.fromtimestamp(end), end - start))


sites = [
    'go.com',
    'vk.com',
    'cnn.com',
    'msn.com',
    'live.com',
    'imdb.com',
    'ebay.com'
]

sites2 = [
    'youku.com',
    'apple.com',
    'imgur.com',
    'yahoo.com',
    'amazon.com',
    'adcash.com',
    'PayPal.com',
    'tumblr.com',
    'reddit.com',
    'blogger.com',
    'dropbox.com',
    'alibaba.com',
    'walmart.com',
    'bestbuy.com',
    'twitter.com',
    'espn.go.com',
    'netflix.com',
    'youtube.com',
    'blogspot.com',
    'flipkart.com',
    'Buzzfeed.com',
    'facebook.com',
    'linkedin.com',
    'microsoft.com',
    'pinterest.com',
    'wordpress.com',
    'instagram.com',
    'aliexpress.com',
    'stackoverflow.com',
    'huffingtonpost.com',
    'Onclickads.net',
    'Cntv.cn',
    'craigslist.org',
    'bbc.co.uk',
    'wikipedia.org',
    'odnoklassniki.ru',
    't.co'
]

TASK_COUNT = 5


def count_chars_at_url(url):
    resp = requests.get(url)
    print('Getting info for the URL {0}'.format(url))
    return (url, len(resp.text))


async def count_chars_at_url_async(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            print('Getting info for the URL {0}'.format(url))
            text = await response.text()
            return (url, len(text))


async def main_async(coroutines):
    await asyncio.wait(coroutines)


def main():
    with timed():
        word_counts = [
            count_chars_at_url('http://' + site) for site in sites
        ]
        print('completed {} tasks'.format(len(sites)))

    with timed():
        coroutines = [
            count_chars_at_url_async(
                'http://' + site) for site in sites
        ]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main_async(coroutines))
        print('completed {} tasks'.format(len(sites)))


if __name__ == "__main__":
    main()
