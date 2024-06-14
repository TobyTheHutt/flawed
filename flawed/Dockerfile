FROM python:3 as python-base

COPY . /usr/src/app/

WORKDIR /usr/src/app

RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

FROM scratch

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

COPY --from=python-base / /

WORKDIR /usr/src/app

ENTRYPOINT ["/usr/local/bin/python", "main.py"]