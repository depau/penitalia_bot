FROM ghcr.io/astral-sh/uv:alpine

# Optimize uv for Docker
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# Install the project's dependencies first to leverage Docker cache
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Add the rest of the project source code
COPY . /app

# Final sync to install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Place the virtual environment's bin on the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Run the bot
ENTRYPOINT ["penitaliabot"]
