from uuid import UUID

import pytest
from pydantic import ValidationError

from bss_web_file_server.models.member import Member


def test_should_create_member():
    url = "url"
    uid = UUID("{12345678-1234-5678-1234-567812345678}")
    member = Member(id=uid, url=url)
    assert member.id is uid
    assert member.url is url


@pytest.mark.parametrize("url", ["", "..", "../escape", "/etc/passwd", "nested/url"])
def test_should_throw_on_path_like_url(url):
    uid = UUID("{12345678-1234-5678-1234-567812345678}")
    with pytest.raises(ValidationError):
        Member(id=uid, url=url)
