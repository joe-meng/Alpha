import pymongo
from scrapy.dupefilter import BaseDupeFilter, logging

logger = logging.getLogger(__name__)


class RFPDupeFilter(BaseDupeFilter):

    def __init__(self, db, collection_name):
        self.db = db
        self.collection = self.db[collection_name]

    @classmethod
    def from_settings(cls, settings, crawler=None):
        client = pymongo.MongoClient(settings['MONGO_URI'])
        db = client[settings['MONGO_DATABASE']]
        collection = settings['MONGO_COLLECTION']
        return cls(db, collection)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings, crawler)

    def request_seen(self, request):
        result = self.collection.find({'url': request.url}).limit(1)
        result = bool(result.count())
        if result:
            logging.info(('seen url in db: %s' % request.url).center(100, '-'))
        return result

    def close(self, reason):
        pass
