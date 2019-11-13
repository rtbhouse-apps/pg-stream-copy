ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION}

ARG UNAME=python
ARG UID=1000
ARG GID=1000
ENV VIRTUAL_ENV=/home/$UNAME/code/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN groupadd -g $GID -o $UNAME \
  && useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

USER $UNAME
WORKDIR /home/$UNAME/code

RUN mkdir -p /home/$UNAME/.cache/pip
VOLUME /home/$UNAME/.cache/pip