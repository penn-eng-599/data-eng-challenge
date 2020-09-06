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
import argparse
import boto3
import logging
import os

from botocore.config import Config
from datetime import datetime

from .api import NHLApi
from .crawler import Crawler
from .storage import Storage, StorageKey
from .transformer import NHLTransformer
from .uuid import UUID

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

def main():

    LOG.info("Starting NHL APP")
    uuid = UUID.get_uuid()

    LOG.info(f"UUID: {uuid}")
    parser = argparse.ArgumentParser(description='NHL Stats crawler')

    # NOTE you can add start_date and end_date arguments
    args = parser.parse_args()

    s3_client = boto3.client(
        's3',
        config=Config(signature_version='s3v4'),
        endpoint_url=os.environ.get('S3_ENDPOINT_URL')
    )
    s3_bucket = os.environ.get('DEST_BUCKET', 'output')
    storage = Storage(s3_client, s3_bucket)

    api = NHLApi()

    # change the start and end date
    start_date = datetime(2017, 10, 1) # TODO make it take args
    end_date = datetime(2017, 10, 1) # TODO make it take args

    LOG.info(f"CRAWLING {start_date} {end_date}")
    crawler = Crawler(api, storage, uuid)
    game_ids = crawler.game_ids(start_date, end_date)
    crawler.crawl(game_ids)
    LOG.info(f"CRAWLING DONE")

    s3_key = NHLApi.BOXSCORE_ENDPOINT
    LOG.info(f"TRANSFORMING DATA")
    nhl_transformer = NHLTransformer(storage, uuid)
    nhl_transformer.transform(game_ids, s3_key)
    LOG.info(f"TRANSFORMING DONE")


if __name__ == '__main__':
    main()
