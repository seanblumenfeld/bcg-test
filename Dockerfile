FROM python:3.7.0

ENV PYTHONUNBUFFERED 1

# Copy requirements file in separately to rest of project.
# This allows docker to cache requirements, and so only changes to
# requirements.txt will trigger a new pip install
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD . /bcg-test
WORKDIR /bcg-test

ENV PYTHONPATH=/bcg-test:$PYTHONPATH
