from pathlib import Path
from uuid import uuid4

import pytest

from bss_web_file_server.models.video import Video
from bss_web_file_server.services.video import VideoService

id = uuid4()
video = Video(id=id, urls=["test_url0", "test_url1"])
updated_video = Video(id=id, urls=["test_url0_updated", "test_url1_updated"])


@pytest.fixture
def video_service(tmp_path):
    """
    Create a video service.
    Initialize the video service with a base path.
    Assert that the id and url paths exist.
    :param tmp_path: a temp directory unique to each test
    :return: video service
    """
    service = VideoService(base_path=str(tmp_path))
    service.create_base_path()
    assert service.id_paths_base.exists()
    assert service.url_paths_base.exists()
    return service


def test_create_folder_structure(video_service):
    video_service.create_folder_structure(video)

    expected_id_path = Path(video_service.id_paths_base, str(video.id))
    assert expected_id_path.exists()
    expected_thumbnail_path = Path(expected_id_path, "thumbnail")
    assert expected_thumbnail_path.exists()
    for url in video.urls:
        expected_url_path = Path(video_service.url_paths_base, url)
        assert expected_url_path.is_symlink()
        assert expected_url_path.resolve() == expected_id_path


def test_update_symlinks(video_service):
    video_service.create_folder_structure(video)

    video_service.update_symlinks(updated_video)

    expected_id_path = Path(video_service.id_paths_base, str(updated_video.id))
    assert expected_id_path.exists()
    for url in updated_video.urls:
        expected_url_path = Path(video_service.url_paths_base, url)
        assert expected_url_path.is_symlink()
        assert expected_url_path.resolve() == expected_id_path
    for url in video.urls:
        assert not Path(video_service.url_paths_base, url).exists()


def test_update_symlink_no_id(video_service):
    with pytest.raises(FileNotFoundError):
        video_service.update_symlinks(video)


def test_create_video_thumbnail(video_service, mocker):
    mock_create_images = mocker.patch(
        "bss_web_file_server.services.video.create_images"
    )
    mock_create_images.return_value = None
    video_service.create_folder_structure(video)

    img_file = b"image"
    video_service.create_thumbnails(img_file, video.id)

    # Assert create_images is called with the correct arguments
    image_folder = Path(video_service.to_id_path(video.id), "thumbnail")
    sizes = [
        (1920, 1080, "fhd"),
        (1280, 720, "hd"),
        (854, 480, "sd"),
    ]
    mock_create_images.assert_called_once_with(img_file, image_folder, sizes)


def test_to_url_path_rejects_path_outside_base(video_service):
    with pytest.raises(ValueError):
        video_service.to_url_path("../escape")
