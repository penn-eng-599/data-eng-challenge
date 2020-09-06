import pytest
  
from datetime import datetime

from nhldata.api import NHLApi
from nhldata.storage import Storage
from nhldata.transformer import NHLTransformer

@pytest.fixture
def transformer_class():
    return NHLTransformer

class TestNHLTransformer:
    def test_init(self, transformer_class):
        storage = Storage(None, None)
        uuid = 1

        transformer = transformer_class(storage, uuid)

        assert transformer.uuid == uuid

    def test_flatten_json(self, transformer_class):
        storage = Storage(None, None)
        uuid = 1

        transformer = transformer_class(storage, uuid)
        json = {
            "a": [
                {
                    "b": [
                        {"c": 1},
                        {"d": 2},
                    ],
                },
                {
                    "bb": [
                        {"cc": 11},
                        {"dd": 22},
                    ],
                },
            ],
        }
        result = transformer.flatten_json(json)
        expected = {
            'player_a_0_b_0_c': 1,
            'player_a_0_b_1_d': 2,
            'player_a_1_bb_0_cc': 11,
            'player_a_1_bb_1_dd': 22,
        }

        assert result == expected
        

