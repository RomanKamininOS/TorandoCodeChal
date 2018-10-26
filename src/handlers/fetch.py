from tornado.httpclient import HTTPError

from utils import db
from handlers.base import BaseHandler
from utils import fetch_url, count_words_in_html, validate_link


class APIFetchLinkHandler(BaseHandler):
    """Fetch data from specified link, saves into db and return words count"""

    async def post(self):
        url = self.json_data.get('url')
        if not validate_link(url):
            raise HTTPError(400)
        html, error = await fetch_url(url)
        if error:
            return self.finish({'error': error.message})
        result = count_words_in_html(html.decode('utf8', errors='ignore'))
        self.finish(result)
        await db.update_words_data(result, self.pool)
