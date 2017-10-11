# -- coding: utf-8 --
import logging

import oss2
from twisted.internet import threads


logger = logging.getLogger(__name__)


class AliOSSFilesStore(object):
    """aliyun oss file storage
    """

    ALI_OSS_ACCESS_KEY_ID = None
    ALI_OSS_ACCESS_KEY_SECRET = None
    ALI_OSS_ENDPOINT = None
    ALI_OSS_BUCKET_NAME = None

    HEADERS = {
        'Cache-Control': 'max-age=172800',
    }

    def __init__(self, uri):
        assert uri.startswith('alioss://')
        self.bucket = oss2.Bucket(
            oss2.Auth(self.ALI_OSS_ACCESS_KEY_ID, self.ALI_OSS_ACCESS_KEY_SECRET),
            self.ALI_OSS_ENDPOINT,
            self.ALI_OSS_BUCKET_NAME
        )

    def stat_file(self, path, info):
        key = path.split('/')[-1]

        def _on_stat_success(res):
            logger.info("%s\n%s", res.status, res.getheaders())
            return res.getheaders()

        return threads.deferToThread(self.bucket.head_object, key).addCallback(_on_stat_success)

    def persist_file(self, path, buf, info, meta=None, headers=None):
        """Upload file to aliyun OSS storage"""
        key = path.split('/')[-1]
        buf.seek(0)
        return threads.deferToThread(self.bucket.put_object, key, buf)