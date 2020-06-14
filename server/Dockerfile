FROM python:3.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y nginx supervisor redis-server vim
RUN pip3 install numpy pyyaml h5py tensorflow keras connexion swagger-ui-bundle Flask-Cors uWSGI redis Pillow

RUN useradd --no-create-home nginx

RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

# Load out config onto the image.
COPY config/nginx.conf /etc/nginx/
COPY config/default.conf /etc/nginx/conf.d/
COPY config/uwsgi.ini /etc/uwsgi/
COPY config/supervisord.conf /etc/supervisor/

RUN mkdir -p /tmp/nginx

RUN mkdir -p /tmp/uploads
RUN chmod 777 /tmp/uploads


# Running as root in case base OS does not have user nginx.
RUN sed -i "s/^user.*/user root;/g" /etc/nginx/nginx.conf

# Redis need to not be daemonized to be started by uwisg
RUN sed -i "s/^daemonize yes/daemonize no/g" /etc/redis/redis.conf

COPY . /usr/src/app

EXPOSE 8085

CMD ["/usr/bin/supervisord"]
