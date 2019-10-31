FROM python:latest

WORKDIR /code
COPY . /code

RUN pip install .[dev,test]
CMD pytest tests/
