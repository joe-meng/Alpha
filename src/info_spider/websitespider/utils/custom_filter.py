# -*- coding:utf-8 -*-
from scrapy.dupefilters import RFPDupeFilter

class SeenURLFilter(RFPDupeFilter):
    """A dupe filter that considers the URL"""
    def __init__(self, path=None):
        pass
        # self.urls_seen = set()
        # RFPDupeFilter.__init__(self, path)

    def request_seen(self, request):
        pass
        # return False
        # if request.url in self.urls_seen:
        #     return True
        # else:
        #     return True
        #     self.urls_seen.add(request.url)
