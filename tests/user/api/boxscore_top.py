#!/usr/bin/env python

import os
import pandas as pd
import pprint
import sys
from datetime import datetime

sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))
from nhldata.app import NHLApi

nhl_api = NHLApi()

game_id = "2018030417"
boxscore_data = nhl_api.boxscore(game_id, True)
pprint.pprint(boxscore_data)
