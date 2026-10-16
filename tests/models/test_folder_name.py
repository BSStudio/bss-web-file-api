import pytest

from bss_web_file_server.models.folder_name import check_folder_name

invalid_names = [
    "",
    ".",
    "..",
    "../escape",
    "/etc/passwd",
    "nested/name",
    "nested\\name",
    "null\0byte",
]


@pytest.mark.parametrize("name", ["url", "szobakoomando-hk", "a.b", "...", "árvíz"])
def test_should_accept_single_folder_name(name):
    assert check_folder_name(name) is name


@pytest.mark.parametrize("name", invalid_names)
def test_should_reject_path_like_name(name):
    with pytest.raises(ValueError):
        check_folder_name(name)
