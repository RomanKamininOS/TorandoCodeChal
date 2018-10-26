import logging
from itertools import islice
from json import JSONDecodeError

from tornado.escape import json_decode
from tornado.web import RequestHandler, HTTPError

LOGGER = logging.getLogger()


class BaseHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.pool = self.application.db_pool

    def paging_offset(self, iterable):
        per_page = int(self.get_argument('per_page', 25))
        page = int(self.get_argument('page', 1))
        if page == 1:
            iterable = islice(iterable, per_page * page)
        else:
            iterable = islice(iterable, per_page * (page - 1), per_page * page)
        return list(iterable)

    @property
    def json_data(self):
        try:
            data = json_decode(self.request.body)
        except JSONDecodeError:
            data = {}
            for key, item in self.request.body_arguments.items():
                data[key] = item[0].decode()
        return data
