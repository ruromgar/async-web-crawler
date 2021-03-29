FROM python:3.7.6-alpine3.11

COPY crawler/ /service/app
COPY common-utils/ /service/common-utils

WORKDIR /service/app

RUN apk add curl build-base npm
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8081

ADD ./crawler/src /service/app/src

ENV PYTHONUNBUFFERED 1

HEALTHCHECK --timeout=30s --interval=1m30s --retries=5 \
  CMD curl -s --fail http://localhost:8081/_health || exit 1
