from __future__ import absolute_import

import logging

from pprint import pformat

from celery import Celery

from tornado.options import define, options, parse_command_line

from flower.app import Flower
from flower.settings import APP_SETTINGS, CELERY_CONFIG

define("port", default=5555, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode", type=bool)
define("inspect", default=True, help="inspect workers", type=bool)


def main(argv=None):
    parse_command_line(argv)
    APP_SETTINGS['debug'] = options.debug

    celery_app = Celery()
    try:
        celery_app.config_from_object(CELERY_CONFIG)
    except ImportError:
        pass

    app = Flower(celery_app=celery_app, **APP_SETTINGS)

    print('> Visit me at http://localhost:%s' % options.port)
    logging.debug('Settings: %s' % pformat(APP_SETTINGS))

    try:
        app.start(options.port, inspect=options.inspect)
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    main()
