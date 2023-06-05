ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim-buster

ARG UNAME=python
ARG UID=1000
ARG GID=1000
ENV POETRY_HOME=/opt/poetry
ENV WORKDIR=/home/$UNAME/code
ENV PATH=$PATH:/home/$UNAME/.local/bin/

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -fr /var/lib/apt/lists/*

RUN python -m pip install --upgrade --no-cache-dir pip==23.1.2

# Install Poetry
ENV POETRY_HOME=/opt/poetry
RUN curl -sSl https://install.python-poetry.org | python - --version 1.5.1 \
    && ln -s ${POETRY_HOME}/bin/poetry /usr/local/bin/poetry

RUN groupadd -g $GID $UNAME \
    && useradd -m -u $UID -g $GID -s /bin/bash $UNAME \
    && mkdir -p $WORKDIR \
    && chown $UNAME:$UNAME $WORKDIR

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.12.0/wait /wait
RUN chmod +x /wait

USER $UNAME
WORKDIR $WORKDIR

COPY --chown=apps ./ $WORKDIR
RUN poetry install --no-ansi --no-interaction --no-root --all-extras

CMD ["poetry", "run", "pytest"]
