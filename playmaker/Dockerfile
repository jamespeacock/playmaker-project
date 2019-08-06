FROM centos:7

ENV LC_ALL en_US.utf8
ENV LANG en_US.utf8

# -- Install Pipenv:
# gcc because we need regex and pyldap
# openldap-devel because we need pyldap
RUN yum update -y \
    && yum install -y https://centos7.iuscommunity.org/ius-release.rpm \
    && yum install -y python36u python36u-libs python36u-devel python36u-pip \
    && yum install -y which gcc \
    && yum install -y openldap-devel \
    && yum install -y git \
    && yum install -y postgresql-devel

RUN curl --silent https://bootstrap.pypa.io/get-pip.py | python3.6

# Backwards compatility.
RUN rm -fr /usr/bin/python3 && ln /usr/bin/python3.6 /usr/bin/python3

RUN pip3 install --upgrade pip
RUN pip3 install pipenv

RUN set -ex && mkdir /app

WORKDIR /app

ADD Pipfile.lock Pipfile.lock
ADD Pipfile Pipfile

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --deploy --system --skip-lock
RUN pip3 freeze

RUN mkdir -p /var/www/static
#RUN ls /app
# COPY startup script into known file location in container
ADD start.sh /start.sh

# EXPOSE port 8000 to allow communication to/from server
EXPOSE 8000

#COPY . /app

# CMD specifcies the command to execute to start the server running.
CMD ["/start.sh"]
# done!
