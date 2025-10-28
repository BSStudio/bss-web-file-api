![GitHub Release Date](https://img.shields.io/github/release-date/BSStudio/bss-web-file-api)
![GitHub Tag](https://img.shields.io/github/v/tag/BSStudio/bss-web-file-api)
![GitHub branch checks state](https://img.shields.io/github/checks-status/BSStudio/bss-web-file-api/main)
![Codecov branch](https://img.shields.io/codecov/c/gh/BSStudio/bss-web-file-api/main)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/BSStudio/bss-web-file-api)
![GitHub](https://img.shields.io/github/license/BSStudio/bss-web-file-api)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=BSStudio_bss-web-file-api&metric=bugs)](https://sonarcloud.io/dashboard?id=BSStudio_bss-web-file-api)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=BSStudio_bss-web-file-api&metric=code_smells)](https://sonarcloud.io/dashboard?id=BSStudio_bss-web-file-api)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=BSStudio_bss-web-file-api&metric=duplicated_lines_density)](https://sonarcloud.io/dashboard?id=BSStudio_bss-web-file-api)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=BSStudio_bss-web-file-api&metric=ncloc)](https://sonarcloud.io/dashboard?id=BSStudio_bss-web-file-api)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=BSStudio_bss-web-file-api&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=BSStudio_bss-web-file-api)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=BSStudio_bss-web-file-api&metric=alert_status)](https://sonarcloud.io/dashboard?id=BSStudio_bss-web-file-api)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=BSStudio_bss-web-file-api&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=BSStudio_bss-web-file-api)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=BSStudio_bss-web-file-api&metric=security_rating)](https://sonarcloud.io/dashboard?id=BSStudio_bss-web-file-api)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=BSStudio_bss-web-file-api&metric=sqale_index)](https://sonarcloud.io/dashboard?id=BSStudio_bss-web-file-api)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=BSStudio_bss-web-file-api&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=BSStudio_bss-web-file-api)

# BSS Web File Server

This project aims to help the video upload process.
It will create folders for each member and video
based on their uuid.

## Development

### Pre-requisites

1. Install python (see version in pyproject.toml)
2. Install poetry

```shell
poetry install
```

### Set up commit hooks

```shell
pre-commit install
```

## Run server

```shell
uvicorn src.bss_web_file_server.main:app
```

### Lint

```shell
poetry run isort . --check
poetry run black . --check
poetry run mypy
poetry run pylint src
```

#### Apply lint

```shell
poetry run isort .
poetry run black .
```

### Run development server

```shell
uvicorn src.bss_web_file_server.main:app --reload
```


### Test

```shell
poetry run pytest
```

### Build docker image

```shell
docker build -t bss_web_file_server .
```

### Run docker compose

```shell
docker-compose up
```
