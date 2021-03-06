FROM python:3.5.2

ENV PHANTOMJS_VERSION 1.9.7

# https://hub.docker.com/r/cmfatih/phantomjs/~/dockerfile/
RUN \
  mkdir -p /srv/var && \
  wget -q --no-check-certificate -O /tmp/phantomjs-$PHANTOMJS_VERSION-linux-x86_64.tar.bz2 https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-$PHANTOMJS_VERSION-linux-x86_64.tar.bz2 && \
  tar -xjf /tmp/phantomjs-$PHANTOMJS_VERSION-linux-x86_64.tar.bz2 -C /tmp && \
  rm -f /tmp/phantomjs-$PHANTOMJS_VERSION-linux-x86_64.tar.bz2 && \
  mv /tmp/phantomjs-$PHANTOMJS_VERSION-linux-x86_64/ /srv/var/phantomjs && \
  ln -s /srv/var/phantomjs/bin/phantomjs /usr/bin/phantomjs

RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -

# Note that we want postgresql-client so 'manage.py dbshell' works.
RUN apt-get update && \
  apt-get install -y nodejs postgresql-client

COPY package.json /calc/

WORKDIR /calc

RUN npm install

ENV PATH /calc/node_modules/.bin:$PATH
ENV DDM_IS_RUNNING_IN_DOCKER yup

COPY requirements.txt /calc/
COPY requirements-dev.txt /calc/

RUN pip install -r /calc/requirements-dev.txt

# The following lines set up our container for being run in a
# cloud environment, where folder sharing is disabled. They're
# irrelevant for a local development environment, where the /calc
# directory will be superseded by a folder share.

COPY . /calc/

RUN gulp build

ENTRYPOINT ["python", "/calc/docker_django_management.py"]
