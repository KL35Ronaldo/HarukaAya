FROM python:3.10-rc-alpine

RUN apk update

RUN apk add --no-cache \
    git \
    postgresql-libs \
    jpeg-dev \
    imagemagick

RUN apk add --no-cache --virtual .build-deps \
    git \
    gcc \
    g++ \
    musl-dev \
    postgresql-dev \
    libffi-dev \
    libwebp-dev \
    zlib-dev \
    imagemagick-dev \
    msttcorefonts-installer \
    fontconfig

# Rust Compiler
RUN apk add cargo

RUN update-ms-fonts && \
    fc-cache -f

RUN mkdir /data

RUN chmod 777 /data

RUN pip install -r https://gitlab.com/HarukaNetwork/OSS/HarukaAya/-/raw/ptb13-revive/requirements.txt

RUN apk del .build-deps

CMD ["python"]
