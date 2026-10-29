ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim

ARG UNAME=python
ARG UID=1000
ARG GID=1000
ENV WORKDIR=/home/$UNAME/code
ENV UV_PROJECT_ENVIRONMENT=/home/$UNAME/venv
ENV UV_PYTHON_DOWNLOADS=never
ENV PATH=/home/$UNAME/venv/bin:$PATH:/home/$UNAME/.local/bin/

COPY --from=ghcr.io/astral-sh/uv:0.13.5 /uv /uvx /bin/

RUN groupadd -g $GID $UNAME \
    && useradd -m -u $UID -g $GID -s /bin/bash $UNAME \
    && mkdir -p $WORKDIR \
    && chown $UNAME:$UNAME $WORKDIR

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.12.0/wait /wait
RUN chmod +x /wait

USER $UNAME
WORKDIR $WORKDIR

COPY --chown=$UNAME pyproject.toml uv.lock $WORKDIR/
RUN uv sync --locked --no-install-project --group dev

COPY --chown=$UNAME ./ $WORKDIR
RUN uv sync --locked --group dev

CMD ["uv", "run", "pytest"]
