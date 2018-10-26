import os
from os import environ as _environ

import rsa
from tornado.options import define, parse_command_line, options, parse_config_file

with open('private.pem', 'rb') as f:
    private = rsa.PrivateKey.load_pkcs1(f.read())

with open('public.pem', 'rb') as f:
    public = rsa.PublicKey.load_pkcs1(f.read())

define('DEBUG', default=_environ.get('DEBUG', True), type=bool, group='application')
define('APP_PORT', default=_environ.get('APP_PORT', 8080), type=int, group='application')

define('MYSQL_HOST', default=_environ.get('MYSQL_HOST', '127.0.0.1'), type=str, group='application')
define('MYSQL_PORT', default=_environ.get('MYSQL_PORT', 3306), type=int, group='application')
define('MYSQL_DATABASE', default=_environ.get('MYSQL_DATABASE', 'tornado_ua'), type=str, group='application')
define('MYSQL_USER', default=_environ.get('MYSQL_USER', 'root'), type=str, group='application')
define('MYSQL_PASSWORD', default=_environ.get('MYSQL_PASSWORD', 'example'), type=str, group='application')

define('MYSQL_CHARSET', default=_environ.get('MYSQL_CHARSET', 'utf8'), type=str, group='application')
define('MYSQL_MAX_CONNECTIONS', default=_environ.get('MYSQL_MAX_CONNECTIONS', 20), type=int, group='application')
define('MYSQL_IDLE_SECONDS', default=_environ.get('MYSQL_IDLE_SECONDS', 7200), type=int, group='application')
define('MYSQL_CONNECTION_TIMEOUT', default=_environ.get('MYSQL_CONNECTION_TIMEOUT', 3), type=int, group='application')


define('SALT', default=_environ.get('SALT', 'XXXXXXXXXX'), type=str, group='application')
define('SECRET_KEY', default=_environ.get('SECRET_KEY', 'XXXXXXXXXX'), type=str, group='application')
define('CONFIG_FILE', default=_environ.get('CONFIG_FILE', 'config.py'), type=str, group='application')
define('template_path', default='./static/', group='application')

define('private_key', default=private, group='application')
define('public_key', default=public, group='application')


def build_app_config(config_file=None):
    config_name = config_file if config_file else options.CONFIG_FILE
    config = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', config_name))
    parse_command_line(final=False)
    if os.path.isfile(config):
        parse_config_file(config, final=False)
