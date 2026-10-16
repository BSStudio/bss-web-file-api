from uuid import UUID

import pytest
from pydantic import ValidationError

from bss_web_file_server.models.video import Video

valid_uid = UUID("{12345678-1234-5678-1234-567812345678}")
valid_urls = ["url1", "url2"]


def test_should_create_video():
    video = Video(id=valid_uid, urls=valid_urls)
    assert video.id is valid_uid
    for i in range(len(valid_urls)):
        assert video.urls[i] is valid_urls[i]


def test_should_throw_on_empty_id():
    with pytest.raises(ValidationError):
        Video(id=None, urls=valid_urls)


def test_should_throw_on_non_uuid():
    with pytest.raises(ValidationError):
        Video(id="uid", urls=valid_urls)


def test_should_throw_on_empty_url_array():
    empty_urls = []
    with pytest.raises(ValidationError):
        Video(id=valid_uid, urls=empty_urls)


@pytest.mark.parametrize("url", ["", "..", "../escape", "/etc/passwd", "nested/url"])
def test_should_throw_on_path_like_url(url):
    with pytest.raises(ValidationError):
        Video(id=valid_uid, urls=["url", url])
