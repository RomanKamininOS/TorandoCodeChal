from tornado.web import StaticFileHandler

from handlers.status import APIStatusHandler
from handlers.fetch import APIFetchLinkHandler
from handlers.admin import APIAdminHandler, HTMLAdminHandler


routes = [(r'/api/v1/fetchWordsData', APIFetchLinkHandler),
          (r'/api/v1/getWordsData', APIAdminHandler),
          (r'/api/v1/status', APIStatusHandler),
          (r'/admin', HTMLAdminHandler),
          (r"/(.*)", StaticFileHandler, {'path': './static',
                                         'default_filename': 'index.html'})
          ]
