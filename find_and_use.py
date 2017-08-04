"""Find working proxies and use them concurrently.

Note: Pay attention to Broker.serve(), instead of the code listed below.
      Perhaps it will be much useful and friendlier.
"""

import asyncio
import logging
from functools import partial
from urllib.parse import urlparse

import aiohttp
import requests

from proxybroker import Broker, ProxyPool
from proxybroker.errors import NoProxyError

def main():
    loop = asyncio.get_event_loop()

    proxies = asyncio.Queue(loop=loop)

    judges = ['http://httpbin.org/get?show_env',
              'https://httpbin.org/get?show_env']
    providers = ['http://www.proxylists.net/', 'https://free-proxy-list.net/']

    broker = Broker(
        proxies, timeout=8, max_conn=200, max_tries=3, verify_ssl=False,
        judges=judges, providers=providers, loop=loop)

    types = [('HTTP', ('Anonymous', 'High')), 'HTTPS']
    countries = ['US', 'DE', 'FR']

    urls = ['http://httpbin.org/get', 'https://httpbin.org/get',
            'http://httpbin.org/redirect/1', 'http://httpbin.org/status/404']

    proxy_pool = ProxyPool(proxies)

    tasks = asyncio.gather(
        broker.find(types=types, countries=countries, post=False,
                    strict=True, limit=100000))
    loop.run_until_complete(tasks)

    broker.show_stats(verbose=True)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='[%H:%M:%S]', level=logging.INFO)
    logger = logging.getLogger('Parser')

    main()
