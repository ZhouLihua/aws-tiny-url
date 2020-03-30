# TODO implement
import sys
sys.path.append("../")
import time

from lambda_tiny_url_make import generate_short_url
from lambda_tiny_url_query import decode_short_url


def test_short_url_pass():
    uuid = int(time.time())
    short_url = generate_short_url(uuid)
    uuid_decode = decode_short_url(short_url)
    assert uuid == uuid_decode


def test_short_url_fail():
    uuid = int(time.time())
    uuid_fake = uuid + 12
    short_url = generate_short_url(uuid)
    uuid_decode = decode_short_url(short_url)
    assert uuid_fake != uuid_decode
