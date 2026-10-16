from pathlib import Path

import pytest

from bss_web_file_server.services.paths import child_path


def test_should_return_entry_inside_base(tmp_path):
    assert child_path(tmp_path, "url") == Path(tmp_path, "url")


@pytest.mark.parametrize("name", ["", ".", "..", "../escape", "/etc/passwd"])
def test_should_reject_name_outside_base(tmp_path, name):
    with pytest.raises(ValueError, match="points outside"):
        child_path(tmp_path, name)


@pytest.mark.parametrize(
    "name", ["nested/name", "nested/../url", "nested\\name", "null\0byte"]
)
def test_should_reject_name_with_several_components(tmp_path, name):
    with pytest.raises(ValueError, match="single folder name"):
        child_path(tmp_path, name)
