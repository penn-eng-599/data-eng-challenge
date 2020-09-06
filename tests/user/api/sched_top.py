#!/usr/bin/env python

import os
import pandas as pd
import pprint
import sys
from datetime import datetime

sys.path.append(os.path.join(sys.path[0], "..", "..", ".."))
from nhldata.app import NHLApi

nhl_api = NHLApi()

start_date = datetime(2019, 2, 1)
end_date = datetime(2019, 2, 2)

sched_data = nhl_api.schedule(start_date, end_date, True)
pprint.pprint(sched_data)
