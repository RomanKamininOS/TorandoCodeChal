import logging

from tornado.httpclient import HTTPError

from utils.db import get_words_data
from handlers.base import BaseHandler


class APIAdminHandler(BaseHandler):
    """Fetch data from specified link, saves into db and return words count"""

    async def get(self):
        words = await get_words_data(self.pool)
        self.finish({'words': words})


class HTMLAdminHandler(BaseHandler):
    """Renders admin page's template"""

    async def get(self):
        self.render("../static/admin.html")
