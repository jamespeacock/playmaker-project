FROM heroku/heroku:18-build

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# -- Install Pipenv:
RUN apt update && apt upgrade -y && apt install python3.6-dev -y
RUN curl --silent https://bootstrap.pypa.io/get-pip.py | python3.6

# Backwards compatility.
RUN rm -fr /usr/bin/python3 && ln /usr/bin/python3.6 /usr/bin/python3

RUN pip3 install pipenv

RUN set -ex && mkdir /app

WORKDIR /playmaker

ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock

RUN pip install pipenv
RUN pipenv lock -v
RUN pip3 freeze
ONBUILD RUN set -ex && pipenv install --deploy --system

# COPY startup script into known file location in container
ADD start.sh /start.sh

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000

# CMD specifcies the command to execute to start the server running.
CMD ["/start.sh"]
# done!
