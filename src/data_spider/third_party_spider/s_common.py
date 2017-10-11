# -- coding: utf-8 --
from datetime import date, timedelta

import logging
from django.db import close_old_connections


logger = logging.getLogger(__name__)


class Spider(object):

    scheduling_stratety = None
    scheduling_param = None

    def __init__(self, date_end=None, date_start=None):
        self.date_end = date_end or date.today()
        self.date_start = date_start or (self.date_end - timedelta(days=3))

    def run(self):
        try:
            self._run()
        except Exception as e:
            logger.error('%s failed: %s' % (self.__class__.__name__, e.args))
        finally:
            close_old_connections()

    def _run(self):
        raise NotImplementedError
