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

WORKDIR /app

ADD Pipfile.lock Pipfile.lock
ADD Pipfile Pipfile

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --deploy --system --skip-lock
RUN pip3 freeze

RUN mkdir -p /app/static
RUN mkdir -p /var/www/static
#RUN ls /app
#RUN python3.6 /app/manage.py collectstatic
# COPY startup script into known file location in container
ADD start.sh /start.sh

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000

#COPY . /app

# CMD specifcies the command to execute to start the server running.
CMD ["/start.sh"]
# done!
