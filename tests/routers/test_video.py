import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bss_web_file_server.models.video import Video
from bss_web_file_server.routers import video


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(video.router)
    return TestClient(app)


video_object = Video(
    id="00000000-0000-0000-0000-000000000000", urls=["szobakoomando-hk"]
)


def test_create_video_folder(client, mocker):
    service_mock = mocker.patch("bss_web_file_server.routers.video.service")
    service_mock.create_folder_structure.return_value = None

    video_data = {"id": str(video_object.id), "urls": video_object.urls}

    response = client.post("/api/v1/video", json=video_data, auth=("admin", "password"))

    assert service_mock.create_folder_structure.call_count == 1
    assert service_mock.create_folder_structure.call_args[0][0] == video_object
    assert response.status_code == 200
    assert response.json() == video_data


def test_update_video_folder_no_id(client, mocker):
    service_mock = mocker.patch("bss_web_file_server.routers.video.service")
    service_mock.to_id_path.return_value.exists.return_value = False

    video_data = {"id": str(video_object.id), "urls": video_object.urls}

    response = client.put("/api/v1/video", json=video_data, auth=("admin", "password"))

    assert service_mock.update_symlinks.call_count == 0
    assert response.status_code == 404


def test_update_video_folder(client, mocker):
    service_mock = mocker.patch("bss_web_file_server.routers.video.service")
    service_mock.to_id_path.return_value.exists.return_value = True
    service_mock.update_symlinks.return_value = None

    video_data = {"id": str(video_object.id), "urls": video_object.urls}

    response = client.put("/api/v1/video", json=video_data, auth=("admin", "password"))

    assert service_mock.update_symlinks.call_count == 1
    assert service_mock.update_symlinks.call_args[0][0] == video_object
    assert response.status_code == 200
    assert response.json() == video_data


def test_upload_video_poster_no_id(client, mocker):
    service_mock = mocker.patch("bss_web_file_server.routers.video.service")
    service_mock.to_id_path.return_value.exists.return_value = False

    response = client.post(
        f"/api/v1/video/{video_object.id}/thumbnail",
        files={"file": ("file.jpg", "file_content", "text/plain")},
        auth=("admin", "password"),
    )

    assert service_mock.create_thumbnail.call_count == 0
    assert response.status_code == 404


def test_upload_video_poster_not_image(client, mocker):
    service_mock = mocker.patch("bss_web_file_server.routers.video.service")
    service_mock.to_id_path.return_value.exists.return_value = True

    response = client.post(
        f"/api/v1/video/{video_object.id}/thumbnail",
        files={"file": ("file.jpg", b"file_content", "text/plain")},
        auth=("admin", "password"),
    )

    assert service_mock.create_thumbnail.call_count == 0
    assert response.status_code == 500
    assert response.text == "Mime is not an image format"


def test_upload_video_poster(client, mocker):
    service_mock = mocker.patch("bss_web_file_server.routers.video.service")
    service_mock.to_id_path.return_value.exists.return_value = True
    service_mock.create_thumbnails.return_value = None

    response = client.post(
        f"/api/v1/video/{video_object.id}/thumbnail",
        files={"file": ("file.jpg", b"file_content", "image/jpeg")},
        auth=("admin", "password"),
    )

    assert service_mock.create_thumbnails.call_count == 1
    assert service_mock.create_thumbnails.call_args[0][0] == b"file_content"
    assert service_mock.create_thumbnails.call_args[0][1] == video_object.id
    assert response.status_code == 200
    assert response.json() == str(video_object.id)


@pytest.mark.parametrize("url", ["../escape", "/etc/passwd", "nested/url"])
def test_update_video_folder_rejects_path_like_url(client, mocker, url):
    service_mock = mocker.patch("bss_web_file_server.routers.video.service")

    video_data = {"id": str(video_object.id), "urls": ["szobakoomando-hk", url]}

    response = client.put("/api/v1/video", json=video_data, auth=("admin", "password"))

    assert response.status_code == 422
    assert service_mock.update_symlinks.call_count == 0
