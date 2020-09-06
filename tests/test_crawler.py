import pytest
  
from datetime import datetime

from nhldata.api import NHLApi
from nhldata.storage import Storage
from nhldata.crawler import Crawler

@pytest.fixture
def crawler_class():
    return Crawler

class TestCrawler:
    def test_init(self, crawler_class):
        nhl_api = NHLApi()
        storage = Storage(None, None)
        uuid = 1

        crawler = crawler_class(nhl_api, storage, uuid)

        assert crawler.uuid == uuid


