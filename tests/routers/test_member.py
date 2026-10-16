import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bss_web_file_server.models.member import Member
from bss_web_file_server.routers import member


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(member.router)
    return TestClient(app)


member_object = Member(id="00000000-0000-0000-0000-000000000000", url="bcsik")


def test_create_member_folder(client, mocker):
    service_mock = mocker.patch("bss_web_file_server.routers.member.service")
    service_mock.create_folder_structure.return_value = None

    member_data = {"id": str(member_object.id), "url": member_object.url}

    response = client.post(
        "/api/v1/member", json=member_data, auth=("admin", "password")
    )

    assert response.status_code == 200
    assert response.json() == member_data
    assert service_mock.create_folder_structure.call_count == 1
    assert service_mock.create_folder_structure.call_args[0][0] == member_object


def test_update_member_folder_no_id(client, mocker):
    service_mock = mocker.patch("bss_web_file_server.routers.member.service")
    service_mock.to_id_path.return_value.exists.return_value = False

    member_data = {"id": str(member_object.id), "url": member_object.url}

    response = client.put(
        "/api/v1/member", json=member_data, auth=("admin", "password")
    )

    assert service_mock.update_symlink.call_count == 0
    assert response.status_code == 404


def test_update_member_folder(client, mocker):
    service_mock = mocker.patch("bss_web_file_server.routers.member.service")
    service_mock.to_id_path.return_value.exists.return_value = True
    service_mock.update_symlink.return_value = None

    member_data = {"id": str(member_object.id), "url": member_object.url}

    response = client.put(
        "/api/v1/member", json=member_data, auth=("admin", "password")
    )

    assert service_mock.update_symlink.call_count == 1
    assert service_mock.update_symlink.call_args[0][0] == member_object
    assert response.status_code == 200
    assert response.json() == member_data


def test_upload_member_picture_no_id(client, mocker):
    service_mock = mocker.patch("bss_web_file_server.routers.member.service")
    service_mock.to_id_path.return_value.exists.return_value = False

    response = client.post(
        f"/api/v1/member/{member_object.id}/profilePicture",
        files={"file": ("file.jpg", "file_content", "image/jpeg")},
        auth=("admin", "password"),
    )

    assert service_mock.create_profile_picture.call_count == 0
    assert response.status_code == 404


def test_upload_member_picture_not_image(client, mocker):
    service_mock = mocker.patch("bss_web_file_server.routers.member.service")
    service_mock.to_id_path.return_value.exists.return_value = True

    response = client.post(
        f"/api/v1/member/{member_object.id}/profilePicture",
        files={"file": ("file.jpg", "file_content", "text/plain")},
        auth=("admin", "password"),
    )

    assert service_mock.create_profile_picture.call_count == 0
    assert response.status_code == 500
    assert response.text == "Mime is not an image format"


def test_upload_member_picture(client, mocker):
    service_mock = mocker.patch("bss_web_file_server.routers.member.service")
    service_mock.to_id_path.return_value.exists.return_value = True
    service_mock.create_profile_picture.return_value = None

    response = client.post(
        f"/api/v1/member/{member_object.id}/profilePicture",
        files={"file": ("file.jpg", "file_content", "image/jpeg")},
        auth=("admin", "password"),
    )

    assert service_mock.create_profile_picture.call_count == 1
    assert service_mock.create_profile_picture.call_args[0][0] == b"file_content"
    assert service_mock.create_profile_picture.call_args[0][1] == member_object.id
    assert response.status_code == 200
    assert response.json() == str(member_object.id)


@pytest.mark.parametrize("url", ["../escape", "/etc/passwd", "nested/url"])
def test_create_member_folder_rejects_path_like_url(client, mocker, url):
    service_mock = mocker.patch("bss_web_file_server.routers.member.service")

    member_data = {"id": str(member_object.id), "url": url}

    response = client.post(
        "/api/v1/member", json=member_data, auth=("admin", "password")
    )

    assert response.status_code == 422
    assert service_mock.create_folder_structure.call_count == 0
