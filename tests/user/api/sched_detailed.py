#!/usr/bin/env python

import os
import pandas as pd
import pprint
import sys
from datetime import datetime

sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))
from nhldata.app import NHLApi

nhl_api = NHLApi()

start_date = datetime(2020, 8, 4)
end_date = datetime(2020, 8, 10)

schedule_data = nhl_api.schedule(start_date, end_date)

if schedule_data.get("dates") is not None:
    for schedule in schedule_data["dates"]:
        for game in schedule["games"]:
            pprint.pprint(schedule["date"])
            pprint.pprint(game)


