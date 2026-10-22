FROM python:3.15.1-alpine@sha256:54448f67d7c31c39e5cdd3ea2d6382395ce142806c284425f8e897d78a0465b3 AS python

FROM python AS builder

COPY --from=ghcr.io/astral-sh/uv:0.13.5@sha256:32a7bb39b496babbd997b0a39a4d66c126bdaf5661b302bf6f06abda8deca6ff /uv /uvx /bin/

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app

# Synchronize DEPENDENCIES without the application itself.
# This layer is cached until uv.lock or pyproject.toml change,
# which are only temporarily mounted into the build container
# since we don't need them in the production one.
# You can create `/app` using `uv venv` in a separate `RUN`
# step to have it cached, but with uv it's so fast, it's not worth
# it, so we let `uv sync` create it for us automagically.
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev --no-install-project

COPY ./src /src

# Install the application into the build environment.
# We won't need the source code in the production image,
# only the installed packages.
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev --no-editable

FROM python AS app

# Add the virtualenv to PATH
ENV PATH="/app/bin:${PATH}"

# Create a non-root user and drop pip/ensurepip, so nothing can be installed at runtime
RUN addgroup -g 1001 -S nonroot && adduser -u 1001 -S nonroot -G nonroot \
    && rm -rf /usr/local/bin/pip* /usr/local/lib/python3.15/ensurepip /usr/local/lib/python3.15/site-packages/pip*

# Copy the pre-built /app virtualenv; it stays root-owned, so the app cannot modify its own code
COPY --from=builder /app /app

USER 1001:1001
WORKDIR /app

ENV SERVER_BASE_PATH="/home/nonroot/assets"
HEALTHCHECK --interval=10s --timeout=5s --start-period=2s --retries=5 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=3)"]
CMD ["fastapi", "run", "--entrypoint", "bss_web_file_server.main:app"]

EXPOSE 8000
