import logging

from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError


async def fetch_url(url):
    err, data = None, None
    http_client = AsyncHTTPClient()
    request = HTTPRequest(url)
    logging.info(url)
    try:
        response = await http_client.fetch(request)
        logging.warning(response.error)
        logging.info(response)
    except HTTPError as e:
        err = e
    else:
        data = response.body
    return data, err


