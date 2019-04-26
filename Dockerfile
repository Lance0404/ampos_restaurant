FROM            python:3.6
MAINTAINER Lance Chang <virtuouslycan@gmail.com>

# Project Files and Settings
#ARG PROJECT_DIR=/usr/src/app
WORKDIR /usr/src/app
COPY Pipfile Pipfile.lock ./
RUN pip install -U pipenv
RUN pipenv install --system
RUN mkdir -p /var/log/ampos
COPY . .
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
