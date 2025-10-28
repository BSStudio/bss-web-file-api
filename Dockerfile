FROM python:3.12.12@sha256:872565c5ac89cafbab19419c699d80bda96e9d0f47a4790e5229bd3aeeeb5da9 AS builder

COPY --from=ghcr.io/astral-sh/uv:0.9.5 /uv /uvx /bin/

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

COPY . /src
WORKDIR /src

# Install the application into the build environment.
# We won't need the source code in the production image,
# only the installed packages.
RUN --mount=type=cache,target=/root/.cache \
    uv sync --locked --no-dev --no-editable


FROM python:3.12-slim@sha256:e97cf9a2e84d604941d9902f00616db7466ff302af4b1c3c67fb7c522efa8ed9 AS app

# Add the virtualenv to PATH
ENV PATH="/app/bin:${PATH}"

# Create a non-root user
RUN adduser --system --group --no-create-home nonroot

# Copy the pre-built /app virtualenv and change ownership to nonroot
COPY --from=builder --chown=nonroot:nonroot /app /app

USER nonroot:nonroot
WORKDIR /app

ENV SERVER_BASE_PATH="/app/assets"
CMD ["uvicorn", "bss_web_file_server.main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80
