import pytest
  
from datetime import datetime
from nhldata.storage import Storage

@pytest.fixture
def storage_class():
    return Storage

class TestStorage:
    def test_init(self, storage_class):
        dest_bucket = "test_bucket"
        s3_client = None

        storage = storage_class(s3_client, dest_bucket)
        
        assert storage.bucket == dest_bucket

    def test_key(self, storage_class):
        pass

