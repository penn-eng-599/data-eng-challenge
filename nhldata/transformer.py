import json
import logging
import os
import pandas as pd

from datetime import datetime

from .storage import Storage, StorageKey

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

COLUMNS = [
    "player_person_id",
    "player_jerseynumber",
    "player_person_active",
    "player_person_alternatecaptain",
    "player_person_birthcity",
    "player_person_birthcountry",
    "player_person_birthdate",
    "player_person_birthstateprovince",
    "player_person_captain",
    "player_person_currentage",
    "player_person_currentteam_id",
    "player_person_currentteam_link",
    "player_person_currentteam_name",
    "player_person_firstname",
    "player_person_fullname",
    "player_person_height",
    "player_person_lastname",
    "player_person_link",
    "player_person_nationality",
    "player_person_primarynumber",
    "player_person_primaryposition_abbreviation",
    "player_person_primaryposition_code",
    "player_person_primaryposition_name",
    "player_person_primaryposition_type",
    "player_person_rookie",
    "player_person_rosterstatus",
    "player_person_shootscatches",
    "player_person_weight",
    "player_position_abbreviation",
    "player_position_code",
    "player_position_name",
    "player_position_type",
    "player_stats_goaliestats_assists",
    "player_stats_goaliestats_decision",
    "player_stats_goaliestats_evensaves",
    "player_stats_goaliestats_evenshotsagainst",
    "player_stats_goaliestats_evenstrengthsavepercentage",
    "player_stats_goaliestats_goals",
    "player_stats_goaliestats_pim",
    "player_stats_goaliestats_powerplaysavepercentage",
    "player_stats_goaliestats_powerplaysaves",
    "player_stats_goaliestats_powerplayshotsagainst",
    "player_stats_goaliestats_savepercentage",
    "player_stats_goaliestats_saves",
    "player_stats_goaliestats_shorthandedsavepercentage",
    "player_stats_goaliestats_shorthandedsaves",
    "player_stats_goaliestats_shorthandedshotsagainst",
    "player_stats_goaliestats_shots",
    "player_stats_goaliestats_timeonice",
    "player_stats_skaterstats_assists",
    "player_stats_skaterstats_blocked",
    "player_stats_skaterstats_eventimeonice",
    "player_stats_skaterstats_faceoffpct",
    "player_stats_skaterstats_faceoffwins",
    "player_stats_skaterstats_faceofftaken",
    "player_stats_skaterstats_giveaways",
    "player_stats_skaterstats_goals",
    "player_stats_skaterstats_hits",
    "player_stats_skaterstats_penaltyminutes",
    "player_stats_skaterstats_plusminus",
    "player_stats_skaterstats_powerplayassists",
    "player_stats_skaterstats_powerplaygoals",
    "player_stats_skaterstats_powerplaytimeonice",
    "player_stats_skaterstats_shorthandedassists",
    "player_stats_skaterstats_shorthandedgoals",
    "player_stats_skaterstats_shorthandedtimeonice",
    "player_stats_skaterstats_shots",
    "player_stats_skaterstats_takeaways",
    "player_stats_skaterstats_timeonice",
    "side",
]


class NHLTransformer:
    DEFAULT_DL_DIR = "/tmp/tr/dl"
    DEFAULT_UP_DIR = "/tmp/tr/up"

    def __init__(self, storage: Storage, uuid: str):
        self.storage = storage
        self.uuid = uuid

    def transform(self, game_ids: list, s3_key: str) -> None:
        """Transforms the data and then saves to s3.

        Args:
            game_ids: list of NHL gamePks
            s3_key: s3 key
        """
        for game_id in game_ids:
            storage_key = StorageKey(
                s3_key=s3_key.format(game_id=game_id),
                ext=".json",
                uuid=self.uuid,
                raw=True,
            )
            dl_filename = f"{self.DEFAULT_DL_DIR}/{storage_key.key()}"

            try:
                self.storage.download(
                    storage_key=storage_key,
                    filename=dl_filename,
                    uuid=self.uuid,
                )
            except Exception as e:
                LOG.error(e)
                LOG.error(f"Could not download {dl_filename}")
                continue

            with open(dl_filename, "r") as f:
                raw_json = json.load(f)


            LOG.info(f"parsing {dl_filename}")
            try:
                df_trans = self.parse(raw_json)
            except Exception as e:
                LOG.error(e)
                LOG.error(f"could not parse data")
                continue

            storage_key = StorageKey(
                s3_key=s3_key.format(game_id=game_id),
                ext=".csv",
                raw=False,
            )


            try:
                upload_filename = f"{self.DEFAULT_UP_DIR}/{storage_key.key()}"
                tmp_dir, _ = upload_filename.rsplit("/", 1)
                if not os.path.exists(tmp_dir):
                    os.makedirs(tmp_dir)

                LOG.info(f"saving {upload_filename}")
                df_trans.to_csv(upload_filename, index=False)
                self.storage.upload(
                    storage_key,
                    upload_filename,
                )
            except Exception as e:
                LOG.error(e)
                LOG.error(f"Could not upload {upload_filename}")
                continue

    def parse(self, raw_json):
        """Parses raw json data into tabular format.

        Args:
            raw_json: json as python object

        Returns:
            flattened json object as pandas DataFrame
        """

        sides = ["home", "away"]
        players = []
        for side in sides:
            all_players = raw_json["teams"][side]["players"]
            for key, player_data in all_players.items():
                result = self.flatten_json(player_data)
                result["side"] = side
                players.append(result)

        # NOTE order the columns
        # preserve the int type
        # fill missing as -1
        df = pd.DataFrame(players, columns=COLUMNS)
        int_cols = {
            "player_person_id": "int32",
            "player_jerseynumber": "int32",
            "player_person_currentage": "int32",
            "player_person_currentteam_id": "int32",
            "player_person_primarynumber": "int32",
        }
        df[list(int_cols.keys())] = df[list(int_cols.keys())].fillna(-1)
        df = df.astype(int_cols)

        return df

    def flatten_json(self, json):
        """Flattens a nested json python object.
        
        Args:
            json: json as python object

        Returns:
            dict of flattened json object
        """
        result = {}
    
        def flatten(obj, name=''):
            if type(obj) is dict:
                for key, value in obj.items():
                    flatten(value, name + key + '_')
            elif type(obj) is list:
                for i, elem in enumerate(obj):
                    flatten(elem, name + str(i) + '_')
            else:
                result[name[:-1].lower()] = obj
    
        flatten(json, "player_")
        return result
