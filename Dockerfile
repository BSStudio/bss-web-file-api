FROM python:3.13 AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on

COPY ./pyproject.toml ./poetry.lock ./
COPY ./src/bss_web_file_server/__init__.py ./src/bss_web_file_server/
RUN pip wheel --wheel-dir ./wheels .


FROM python:3.13-slim AS app

# Create a non-root user
RUN adduser --system --group --home /home/nonroot nonroot
ENV PATH="/home/nonroot/.local/bin:${PATH}"
USER nonroot:nonroot
WORKDIR /home/nonroot/app

COPY --from=builder /app ./
COPY ./src ./src

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install --no-cache-dir ./wheels/*

ENV SERVER_BASE_PATH="/home/nonroot/assets"
CMD ["uvicorn", "src.bss_web_file_server.main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80
LABEL org.opencontainers.image.source="https://github.com/BSStudio/bss-web-file-api"
LABEL org.opencontainers.image.description="BSS Web file API"
LABEL org.opencontainers.image.licenses="GPL-3.0"
