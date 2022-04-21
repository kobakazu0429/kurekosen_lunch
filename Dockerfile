FROM python:3.10

ARG API_KEY
ARG API_KEY_SECRET
ARG ACCESS_TOKEN
ARG ACCESS_TOKEN_SECRET

ENV API_KEY=${API_KEY}
ENV API_KEY_SECRET=${API_KEY_SECRET}
ENV ACCESS_TOKEN=${ACCESS_TOKEN}
ENV ACCESS_TOKEN_SECRET=${ACCESS_TOKEN_SECRET}

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9

RUN apt update && \
  apt install -y --no-install-recommends locales default-jdk && \
  rm -rf /var/lib/apt/lists/*

RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY . /tmp/
RUN python3 /tmp/main.py
