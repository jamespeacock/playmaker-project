FROM ubuntu:20.04

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Install ubuntu deps
RUN apt-get update
RUN apt-get -yqq install libpq-dev build-essential python3-dev python3-setuptools python3-wheel curl git 

# -- Install Pipenv:
RUN curl --silent https://bootstrap.pypa.io/get-pip.py | python3.8

RUN pip3 install --upgrade pip
RUN pip3 install pipenv

RUN set -ex && mkdir /app

WORKDIR /app

ADD Pipfile.lock Pipfile.lock
ADD Pipfile Pipfile

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system
RUN pip3 freeze

# COPY startup script into known file location in container
ADD start.sh /start.sh
ADD . /app

RUN mkdir -p /var/www/static
RUN mkdir -p /static
RUN python3.8 /app/manage.py collectstatic --noinput

EXPOSE 5000

CMD ["/start.sh"]
# done!
