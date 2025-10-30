import os

import pytest
import requests
from testcontainers.compose import DockerCompose
from testcontainers.core.wait_strategies import LogMessageWaitStrategy


@pytest.fixture(scope="session")
def compose():
    print("Starting compose")
    compose = DockerCompose(
        context=os.getcwd(),
        compose_file_name="docker-compose.yml",
        build=True,
    )
    compose.waiting_for({"app": LogMessageWaitStrategy("8000")})
    compose.start()
    yield compose
    compose.stop()


def test_health(compose: DockerCompose):
    host = compose.get_service_host("app")
    port = compose.get_service_port("app", 8000)
    assert "Application startup complete." in compose.get_logs("app")[0]
    response = requests.get(f"http://{host}:{port}/health")
    assert response.status_code == 200
    assert response.text == "UP"


def test_ping(compose: DockerCompose):
    host = compose.get_service_host("app")
    port = compose.get_service_port("app", 8000)
    response = requests.get(f"http://{host}:{port}/ping")
    assert response.status_code == 200
    assert response.text == "PONG"
