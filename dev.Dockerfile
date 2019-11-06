FROM python:3.8

ARG UNAME=python
ARG UID=1000
ARG GID=1000
ENV PATH="/home/$UNAME/.local/bin:$PATH"

RUN groupadd -g $GID -o $UNAME \
  && useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

USER $UNAME
WORKDIR /home/$UNAME/code

RUN mkdir /home/$UNAME/.local/
VOLUME /home/$UNAME/.local/