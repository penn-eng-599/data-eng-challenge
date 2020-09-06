import logging

from datetime import datetime

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

class UUID:
    @staticmethod
    def get_uuid():
        return datetime.utcnow().strftime("%Y%m%d_%H%m%S")


