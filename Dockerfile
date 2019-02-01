FROM alpine
MAINTAINER vincent <digitalsin.gmx.com>

WORKDIR /apps
COPY . /apps

RUN apk update \
    && apk add python python-dev py2-pip build-base \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm -rf /var/cache/apk/*

EXPOSE 5000

ENV FLASK_APP=/apps/PySim/main.py
WORKDIR /apps/PySim

CMD ["flask", "run", "--host=0.0.0.0" ]