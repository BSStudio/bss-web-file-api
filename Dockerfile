FROM python:3.14.7-alpine@sha256:05b2b8b732ecd268fee8727a369f936f022d1321b59befd13c30ede22769dcdc AS python

FROM python AS builder

COPY --from=ghcr.io/astral-sh/uv:0.12.8@sha256:d1cbaeadc234fe19c0d93daabcf5e98738cd93c6d1dd4918ef6aa30735feb23a /uv /uvx /bin/

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
RUN addgroup -g 1001 -S nonroot && adduser -u 1001 -S nonroot -G nonroot

# Copy the pre-built /app virtualenv and change ownership to nonroot
COPY --from=builder --chown=1001:1001 --chmod=500 /app /app

USER 1001:1001
WORKDIR /app

ENV SERVER_BASE_PATH="/home/nonroot/assets"
CMD ["fastapi", "run", "--entrypoint", "bss_web_file_server.main:app"]

EXPOSE 8000
