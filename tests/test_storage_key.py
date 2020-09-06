import pytest 
  
from datetime import datetime 
from nhldata.storage import StorageKey

@pytest.fixture
def storage_key_class():
    return StorageKey

class TestStorageKey: 
    def test_init(self, storage_key_class): 
        uuid = "1"
        s3_key = "endpoint"
        storage_key = storage_key_class(
            s3_key=s3_key,
            uuid=uuid,
        )

        result = storage_key.uuid
        expected = f"_{uuid}"

        assert result == expected

    def test_key(self, storage_key_class):
        uuid = "1"
        s3_key = "key"
        storage_key = storage_key_class(
            s3_key=s3_key,
            uuid=uuid,
        )

        result = storage_key.key()
        expected = f"raw/{s3_key}_{uuid}"

        assert result == expected



