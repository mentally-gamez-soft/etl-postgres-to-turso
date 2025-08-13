# ==========================================================================================================
# =====================              STAGE 1 - Creation of py wheels                   =====================
# ==========================================================================================================
FROM python:3.12-alpine AS builder

# Install necessary tools 
RUN apk update && apk upgrade --no-interactive
RUN apk add libpq libpq-dev python3-dev build-base linux-headers bash curl lscpu gnupg postgresql-client postgresql-dev gcc make cmake --no-interactive
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# set work directory
WORKDIR /usr/src/py-req 

# set env variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps --wheel-dir ./wheels -r requirements.txt


# ========================================================================================================================
# =====================              FINAL STAGE - Creation of the app with wheels                   =====================
# ========================================================================================================================
FROM python:3.12-alpine

RUN apk update && apk upgrade --no-interactive
RUN apk add libpq curl libpq-dev python3-dev build-base gcc make cmake --no-interactive

# set env variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

LABEL Version=$version_number 

WORKDIR /app

COPY --from=builder /usr/src/py-req/wheels/ ./wheels/
COPY --from=builder /usr/src/py-req/requirements.txt .

RUN pip install --upgrade pip \
&& pip install --no-cache ./wheels/*

# RUN pip install --no-cache libsql-experimental

COPY config ./config
COPY main.py .
COPY core ./core
RUN mkdir ./rsa_keys
RUN mkdir ./logs
# =====================   Managing crontab    =====================
RUN echo ' */2  *  *  *  * python3 /app/main.py dev' >> /etc/crontabs/root

# run crond as main process of container
CMD ["/usr/sbin/crond", "-f"]

