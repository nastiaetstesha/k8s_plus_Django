# FROM nginx/unit:1.25.0-python3.9
# ENV PYTHONUNBUFFERED 1
# ENV PYTHONDONTWRITEBYTECODE 1

# WORKDIR /webapp
# COPY requirements.txt /webapp/
# RUN apt update && apt install -y python3-pip                                  \
#     && pip3 install -r requirements.txt                                       \
#     && apt remove -y python3-pip                                              \
#     && apt autoremove --purge -y                                              \
#     && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list
# COPY unit_config.json /docker-entrypoint.d/
# COPY src /webapp/src
# WORKDIR /webapp/src
# RUN SECRET_KEY=django-insecure-0if40nf4nf93n9 python manage.py collectstatic --noinput
# EXPOSE 80
# VOLUME ["/media"]
# CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]

FROM nginx/unit:1.25.0-python3.9
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/webapp/src

WORKDIR /webapp
COPY requirements.txt /webapp/

RUN apt update && apt install -y python3-pip \
    && pip3 install -r requirements.txt \
    && apt remove -y python3-pip \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

COPY unit_config.json /docker-entrypoint.d/
COPY src /webapp/src
WORKDIR /webapp/src
ENV SECRET_KEY=django-insecure-01f40nf4nf93n9
RUN python manage.py collectstatic --noinput
EXPOSE 80
VOLUME ["/media"]
CMD unitd --no-daemon --control unix:/var/run/control.unit.sock & \
    sleep 2 && \
    curl -X PUT --unix-socket /var/run/control.unit.sock \
         -d @/docker-entrypoint.d/unit_config.json \
         -H 'Content-Type: application/json' \
         http://localhost/config/ && \
    tail -f /dev/null
