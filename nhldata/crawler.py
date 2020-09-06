#!/usr/bin/env python
'''
	This is the NHL crawler.  

Scattered throughout are TODO tips on what to look for.

Assume this job isn't expanding in scope, but pretend it will be pushed into production to run 
automomously.  So feel free to add anywhere (not hinted, this is where we see your though process..)
    * error handling where you see things going wrong.  
    * messaging for monitoring or troubleshooting
    * anything else you think is necessary to have for restful nights
'''
import json
import logging
import os
from datetime import datetime

from .api import NHLApi
from .storage import Storage, StorageKey

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

class Crawler:
    DEFAULT_UP_DIR = "/tmp/raw/up"

    def __init__(self, api: NHLApi, storage: Storage, uuid: str):
        self.api = api
        self.storage = storage
        self.uuid = uuid

    def game_ids(self, start_date: datetime, end_date: datetime) -> None:
        """Get game ids.

        Args:
            start_date: start date of nhl schedule
            end_date: end date of nhl schedule

        Returns:
            list of game ids
        """
        game_ids = self.api.game_ids(start_date, end_date)

        return game_ids
        

    def crawl(self, game_ids: list) -> None:
        """Crawls the api to store data to s3

        Args:
            game_ids: list of game ids
        """
        s3_key = self.api.BOXSCORE_ENDPOINT
        for game_id in game_ids:
            storage_key = StorageKey(
                s3_key=s3_key.format(game_id=game_id),
                ext=".json",
                raw=True,
                uuid = self.uuid,
            )

            boxscore_json = self.api.boxscore(game_id)
            filename = f"{self.DEFAULT_UP_DIR}/{storage_key.key()}"
            tmp_dir, _ = filename.rsplit("/", 1)
            if not os.path.exists(tmp_dir):
                os.makedirs(tmp_dir)

            with open(filename, "w") as f:
                json.dump(boxscore_json, f)

            self.storage.upload(
                storage_key=storage_key,
                filename=filename,
            )

