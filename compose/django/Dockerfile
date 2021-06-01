FROM python:3.8

WORKDIR /app/src

RUN apt-get update && \
    pip install --upgrade pip

COPY requirements /tmp/requirements
RUN cd /tmp/requirements && \
    pip install --no-cache-dir -r main.txt && \
    rm -r /tmp/requirements

COPY compose/django/scripts/ /app/
RUN chmod +x /app/*.sh

COPY backend /app/src
