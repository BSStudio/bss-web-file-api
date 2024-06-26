from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from bss_web_file_server.main import app


def test_main_startup(mocker: MockerFixture):
    mock_video_service = mocker.patch("bss_web_file_server.main.video_service")
    mock_member_service = mocker.patch("bss_web_file_server.main.member_service")
    mock_member_service.create_base_path = mocker.Mock()
    mock_video_service.create_base_path = mocker.Mock()

    with TestClient(app) as client:
        response = client.get("/docs")
        assert response.status_code == 200
    assert mock_video_service.create_base_path.call_count == 1
    assert mock_member_service.create_base_path.call_count == 1
