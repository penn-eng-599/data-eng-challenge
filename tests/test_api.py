import pytest

from datetime import datetime
from nhldata.api import NHLApi

REST_API = "https://statsapi.web.nhl.com/api/v1"

@pytest.fixture
def nhl_api_class():
    return NHLApi

class TestNHLApi:
    def test_init(self, nhl_api_class):
        nhl_api = nhl_api_class()
    
        assert nhl_api.base == REST_API
        assert nhl_api.SCHEDULE_ENDPOINT == "schedule"
        assert nhl_api.BOXSCORE_ENDPOINT == "game/{game_id}/boxscore"
    
    def test_get_method(self, nhl_api_class):
        nhl_api = nhl_api_class()
        url = f"{REST_API}/statTypes"
        params = None
        data = nhl_api._get(url, params)
    
        assert len(data) > 0
    
    def test_url_method(self, nhl_api_class):
        url = "www.somewebsite.com"
        nhl_api = nhl_api_class(url)
        path = "test"

        result = nhl_api._url(path)
        expected = f"{url}/{path}"
    
        assert result == expected
    
    def test_schedule_request(self, nhl_api_class):
        nhl_api = nhl_api_class()
        start_date = datetime(2020, 8, 4)
        end_date = datetime(2020, 8, 5)
        data = nhl_api.schedule(start_date, end_date)
    
        assert "dates" in data.keys()
        assert "games" in data["dates"][0].keys()
    
    def test_boxscore_request(self, nhl_api_class):
        nhl_api = nhl_api_class()
        game_id = "2019030042"
        data = nhl_api.boxscore(game_id)
    
        assert "teams" in data.keys()
        assert "home" in data["teams"].keys()
        assert "away" in data["teams"].keys()
        assert "players" in data["teams"]["home"].keys()
        assert "players" in data["teams"]["away"].keys()
