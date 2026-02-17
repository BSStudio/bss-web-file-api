FROM python:3.14.3-alpine@sha256:faee120f7885a06fcc9677922331391fa690d911c020abb9e8025ff3d908e510 AS python

FROM python AS builder

COPY --from=ghcr.io/astral-sh/uv:0.10.4@sha256:4cac394b6b72846f8a85a7a0e577c6d61d4e17fe2ccee65d9451a8b3c9efb4ac /uv /uvx /bin/

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

# Create a non-root user
RUN addgroup -S nonroot && adduser -S nonroot -G nonroot

# Copy the pre-built /app virtualenv and change ownership to nonroot
COPY --from=builder --chown=nonroot:nonroot --chmod=500 /app /app

USER nonroot:nonroot
WORKDIR /app

ENV SERVER_BASE_PATH="/home/nonroot/assets"
CMD ["fastapi", "run", "--entrypoint", "bss_web_file_server.main:app"]

EXPOSE 8000
