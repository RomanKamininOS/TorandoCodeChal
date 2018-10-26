import logging
import os

import nltk
import tormysql
from tornado import ioloop
from tornado.options import options
from tornado.web import Application

from routes import routes
from settings import build_app_config

settings_path = os.environ.get('CONFIG_PATH')
build_app_config(settings_path)


class WordsCountApplication(Application):

    @property
    def db_pool(self):
        logging.warning('Creating connection pool')
        logging.warning('host {} user {} pass {}'.format(options.MYSQL_HOST,
                                                         options.MYSQL_USER,
                                                         options.MYSQL_PASSWORD,))
        pool = tormysql.helpers.ConnectionPool(
            max_connections=options.MYSQL_MAX_CONNECTIONS,
            idle_seconds=options.MYSQL_IDLE_SECONDS,
            wait_connection_timeout=options.MYSQL_CONNECTION_TIMEOUT,
            host=options.MYSQL_HOST,
            user=options.MYSQL_USER,
            passwd=options.MYSQL_PASSWORD,
            db=options.MYSQL_DATABASE,
            charset=options.MYSQL_CHARSET,
        )
        return pool


def make_app():
    logging.getLogger().setLevel(logging.INFO)
    logging.warning('Application use debug mode: {}'.format(options.DEBUG))
    nltk.data.path.append('./nltk_data')
    app = WordsCountApplication(routes, debug=options.DEBUG)
    return app


def main():
    app = make_app()
    app.listen(options.APP_PORT)
    logging.info('Server start on port: {}'.format(options.APP_PORT))
    try:
        ioloop.IOLoop.current().start()
    except (KeyboardInterrupt, SystemExit):
        logging.info('Server graceful shutdown')
