import logging
from datetime import datetime
import requests

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

class NHLApi:
    SCHEMA_HOST = "https://statsapi.web.nhl.com"
    VERSION_PREFIX = "api/v1"
    SCHEDULE_ENDPOINT = "schedule"
    BOXSCORE_ENDPOINT = "game/{game_id}/boxscore"

    def __init__(self, base=None):
        """Initialize class with the nhl api endpoint."""
        self.base = base if base else f'{self.SCHEMA_HOST}/{self.VERSION_PREFIX}'

    def _url(self, path):
        """Build and return request url.

        Args:
            path: api endpoint

        Returns:
            request url as a string
        """
        return f'{self.base}/{path}'

    def _get(self, url, params=None):
        """Hit request url and get response.

        Args:
            url: request url
            params: params from request library

        Returns:
            response in json of api endpoint
        """

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()

    def schedule(self, start_date: datetime, end_date: datetime) -> dict:
        """Gets NHL schedule data for a date range.

        Note that the schedule day is different from the game date. NHL has
        preseason, regular season, playoffs, and all-start dates.

        preseason happens around Sep
        season start Oct and run to about Jun (end of Stanley cup)

        Thus Aug to Aug seems like a good date range to get all the games

        Ref:
            https://en.wikipedia.org/wiki/Season_structure_of_the_NHL

        Args:
            start_date: schedule start date (inclusive)
            end_date: schedule end date (inclusive)

        Returns:
            schedule data in structure that is like
                "dates": [ 
                    {
                        " #.. meta info, one for each requested date ",
                        "games": [
                            { #.. game info },
                            ...
                        ]
                    },
                    ...
                ]
        """
        schedule_url = self._url(self.SCHEDULE_ENDPOINT)
        params = {
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
        }

        return self._get(url=schedule_url, params=params)

    def boxscore(self, game_id):
        """Gets boxscore data from game_id.

        A box score is a structured summary of the results from a sport
        competition. The boxscore data has information regarding the
        team for a particular match that is identified by the unique game id.

        Args:
            game_id: unique game identifier
                The first 4 digits identify the season of the game
                    (ie. 2017 for the 2017-2018 season).
                The next 2 digits give the type of game,
                    01 = preseason,
                    02 = regular season,
                    03 = playoffs,
                    04 = all-star.
                The final 4 digits identify the specific game number

        Returns:
            boxcore data in structure that is like
               "teams": {
                    "home": {
                        " #.. other meta ",
                        "players": {
                            $player_id: {
                                #... player info
                            },
                            #...
                        }
                    },
                    "away": {
                        #... same as "home" 
                    }
                }
        """
        boxscore_url = self._url(self.BOXSCORE_ENDPOINT.format(game_id=game_id))

        return self._get(url=boxscore_url)

    def game_ids(self, start_date, end_date):
        """Gets a list of game ids scheduled from start date to end date.

        Args:
            start_date: schedule start date (inclusive)
            end_date: schedule end date (inclusive)
        
        """
        sched_data = self.schedule(start_date, end_date)

        game_ids = []
        for sched in sched_data["dates"]:
            for game in sched["games"]:
                game_ids.append(game["gamePk"])

        return game_ids


