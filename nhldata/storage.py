import json
import logging
import os

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

class StorageKey:
    """Class for the s3 storage key."""

    def __init__(self, s3_key: str, ext="", raw=True, uuid: str=None):
        self.s3_key = s3_key.replace("/", "_")
        self.ext = ext
        self.type = "raw" if raw else "trans"
        self.uuid = f"_{uuid}" if uuid else ""

    def key(self):
        """Renders the s3 key for the given set of properties."""
        key = f"{self.type}/{self.s3_key}{self.uuid}{self.ext}"

        return key


class Storage:
    def __init__(self, s3_client, bucket: str):
        """Initialize class with bucket and s3_client."""
        self._s3_client = s3_client
        self.bucket = bucket

    def upload(self, storage_key: StorageKey, filename: str):
        """Uploads file into s3 bucket.

        This will either persist the data to s3 but if anything goes wrong it
        will persis to disk.
        
        Args:
            storage_key: StorageKey object
            filename: file to upload to s3

        Returns:
            True
        
        """
        try:
            key = storage_key.key()

            LOG.info(f"uploading {key}")
            response = self._s3_client.upload_file(
                filename,
                self.bucket,
                key,
            )
            LOG.info(f"uploaded {key}")
        except ClientError as e:
            LOG.error(e)
            LOG.error(f"{filename} was not uploaded to s3.")

    def download(self, storage_key: StorageKey, filename="/tmp/file.ext", uuid=None):
        """Retrieves games from s3 bucket.

        If there is an error nothing will be retrieved

        Args:
            storage_key: StorageKey object
        Returns:
            game data as python object
        """
        try:
            key = storage_key.key()
            tmp_dir, _ = filename.rsplit("/", 1)
            if not os.path.exists(tmp_dir):
                os.makedirs(tmp_dir)

            LOG.info(f"downloading {key} to {filename}")
            self._s3_client.download_file(
                self.bucket,
                key,
                filename,
            )
            LOG.info(f"downloaded {key}")
        except ClientError as e:
            LOG.error(e)
            LOG.error(f"{key} was not retrieved")
            raise

