FROM python:3.8-alpine

RUN apk add git inotify-tools

COPY /docker/cron_script.sh /docker/inotify_script.sh /bin/
COPY /docker/build.crontab /etc/crontabs/root

COPY . /build

RUN pip install /build

CMD ["/bin/inotify_script.sh"]