import pytest
  
from datetime import datetime
from nhldata.uuid import UUID


class TestUUID:
    def test_uuid(self):
        uuid = UUID.get_uuid()
        
        assert isinstance(uuid, str)


