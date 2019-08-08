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

ADD . /app

WORKDIR /app

ADD Pipfile.lock Pipfile.lock
ADD Pipfile Pipfile

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --deploy --system --skip-lock
RUN pip3 freeze

# COPY startup script into known file location in container
ADD start.sh /start.sh

RUN ls /app

EXPOSE 5000

CMD ["/start.sh"]
# done!
