from pathlib import Path
from uuid import uuid4

import pytest

from bss_web_file_server.models.member import Member
from bss_web_file_server.services.member import MemberService

id = uuid4()
member = Member(id=id, url="test_url")
updated_member = Member(id=id, url="test_url_updated")


@pytest.fixture
def member_service(tmp_path):
    """
    Create a member service.
    Initialize the member service with a base path.
    Assert that the id and url paths exist.
    :param tmp_path: a temp directory unique to each test
    :return: member service
    """
    service = MemberService(base_path=str(tmp_path))
    service.create_base_path()
    assert service.id_paths_base.exists()
    assert service.url_paths_base.exists()
    return service


def test_create_folder_structure(member_service):
    member_service.create_folder_structure(member)

    expected_id_path = Path(member_service.id_paths_base, str(member.id))
    assert expected_id_path.exists()
    expected_profile_path = Path(expected_id_path, "profile")
    assert expected_profile_path.exists()
    expected_url_path = Path(member_service.url_paths_base, member.url)
    assert expected_url_path.is_symlink()
    assert expected_url_path.resolve() == expected_id_path


def test_update_symlink(member_service):
    member_service.create_folder_structure(member)

    member_service.update_symlink(updated_member)

    expected_id_path = Path(member_service.id_paths_base, str(updated_member.id))
    assert expected_id_path.exists()
    expected_url_path = Path(member_service.url_paths_base, updated_member.url)
    assert expected_url_path.is_symlink()
    assert expected_url_path.resolve() == expected_id_path
    assert not Path(member_service.url_paths_base, member.url).exists()


def test_update_symlink_no_id(member_service):
    with pytest.raises(FileNotFoundError):
        member_service.update_symlink(member)


def test_create_profile_picture(member_service, mocker):
    mock_create_images = mocker.patch(
        "bss_web_file_server.services.member.create_images"
    )
    mock_create_images.return_value = None
    member_service.create_folder_structure(member)

    img_file = b"image"
    member_service.create_profile_picture(img_file, member.id)

    # Assert create_images is called with the correct arguments
    image_folder = Path(member_service.to_id_path(member.id), "profile")
    sizes = [
        (1920, 1080, "xl"),
        (1280, 720, "l"),
        (854, 480, "m"),
    ]
    mock_create_images.assert_called_once_with(img_file, image_folder, sizes)


def test_to_url_path_rejects_path_outside_base(member_service):
    with pytest.raises(ValueError):
        member_service.to_url_path("../escape")
