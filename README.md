# Django Site

Докеризированный сайт на Django для экспериментов с Kubernetes.

Внутри контейнера Django приложение запускается с помощью Nginx Unit, не путать с Nginx. Сервер Nginx Unit выполняет сразу две функции: как веб-сервер он раздаёт файлы статики и медиа, а в роли сервера-приложений он запускает Python и Django. Таким образом Nginx Unit заменяет собой связку из двух сервисов Nginx и Gunicorn/uWSGI. [Подробнее про Nginx Unit](https://unit.nginx.org/).

## Как подготовить окружение к локальной разработке

Код в репозитории полностью докеризирован, поэтому для запуска приложения вам понадобится Docker. Инструкции по его установке ищите на официальных сайтах:

- [Get Started with Docker](https://www.docker.com/get-started/)

Вместе со свежей версией Docker к вам на компьютер автоматически будет установлен Docker Compose. Дальнейшие инструкции будут его активно использовать.

## Как запустить сайт для локальной разработки

Запустите базу данных и сайт:

```shell
$ docker compose up
```

В новом терминале, не выключая сайт, запустите несколько команд:

```shell
$ docker compose run --rm web ./manage.py migrate  # создаём/обновляем таблицы в БД
$ docker compose run --rm web ./manage.py createsuperuser  # создаём в БД учётку суперпользователя
```

Готово. Сайт будет доступен по адресу [http://127.0.0.1:8080](http://127.0.0.1:8080). Вход в админку находится по адресу [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

## Как вести разработку

Все файлы с кодом django смонтированы внутрь докер-контейнера, чтобы Nginx Unit сразу видел изменения в коде и не требовал постоянно пересборки докер-образа -- достаточно перезапустить сервисы Docker Compose.

### Как обновить приложение из основного репозитория

Чтобы обновить приложение до последней версии подтяните код из центрального окружения и пересоберите докер-образы:

``` shell
$ git pull
$ docker compose build
```

После обновлении кода из репозитория стоит также обновить и схему БД. Вместе с коммитом могли прилететь новые миграции схемы БД, и без них код не запустится.

Чтобы не гадать заведётся код или нет — запускайте при каждом обновлении команду `migrate`. Если найдутся свежие миграции, то команда их применит:

```shell
$ docker compose run --rm web ./manage.py migrate
…
Running migrations:
  No migrations to apply.
```

### Как добавить библиотеку в зависимости

В качестве менеджера пакетов для образа с Django используется pip с файлом requirements.txt. Для установки новой библиотеки достаточно прописать её в файл requirements.txt и запустить сборку докер-образа:

```sh
$ docker compose build web
```

Аналогичным образом можно удалять библиотеки из зависимостей.

<a name="env-variables"></a>
## Переменные окружения

Образ с Django считывает настройки из переменных окружения:

`SECRET_KEY` -- обязательная секретная настройка Django. Это соль для генерации хэшей. Значение может быть любым, важно лишь, чтобы оно никому не было известно. [Документация Django](https://docs.djangoproject.com/en/3.2/ref/settings/#secret-key).

`DEBUG` -- настройка Django для включения отладочного режима. Принимает значения `TRUE` или `FALSE`. [Документация Django](https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-DEBUG).

`ALLOWED_HOSTS` -- настройка Django со списком разрешённых адресов. Если запрос прилетит на другой адрес, то сайт ответит ошибкой 400. Можно перечислить несколько адресов через запятую, например `127.0.0.1,192.168.0.1,site.test`. [Документация Django](https://docs.djangoproject.com/en/3.2/ref/settings/#allowed-hosts).

`DATABASE_URL` -- адрес для подключения к базе данных PostgreSQL. Другие СУБД сайт не поддерживает. [Формат записи](https://github.com/jacobian/dj-database-url#url-schema).

### ⚙️ Развёртывание

## 1. Запустить Minikube:

```
minikube start
```
## Установи Ingress Controller:


`minikube addons enable ingress`
## Добавь домен в /etc/hosts:

`sudo nano /etc/hosts`
Добавь строчку:

`127.0.0.1 star-burger.test`

## Установи PostgreSQL через Helm:
```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install pg-db bitnami/postgresql --set auth.database=starburger --set auth.username=starburger
```
## 2. Применить секреты и манифесты:
```
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/
```
## Запусти миграции:

`kubectl apply -f kubernetes/migrate.yaml`
## 3. Открыть сайт:
`minikube tunnel`

# В другом окне
`open http://star-burger.test`


## Очистка сессий
Регулярная задача очищает устаревшие сессии через CronJob:

- Файл: `kubernetes/clearsessions-cronjob.yaml`
- Запускается каждый день в полночь
- Принудительный запуск:

```
kubectl create job --from=cronjob/clearsessions clearsessions-once
```
## Проверка статуса
```
kubectl get ingress
kubectl get svc
kubectl get pods
kubectl describe ingress django-ingress
```

| Файл                         | Назначение                                                                              |
| ---------------------------- | --------------------------------------------------------------------------------------- |
| `deployment.yaml`            | Разворачивает основное Django-приложение. Указывает образ, переменные окружения и порт. |
| `service.yaml`               | Описывает ClusterIP-сервис для Django, через который работает Ingress.                  |
| `ingress.yaml`               | Настраивает доменное имя (`star-burger.test`) и маршрут на `service`.                   |
| `pod.yaml`                   | (Дополнительно) пример одиночного Pod-а, используется для отладки.                      |
| `secret.yaml`                | Хранит переменные окружения, включая `SECRET_KEY` и `DATABASE_URL`.                     |
| `clearsessions.yaml`         | Job для ручовой очистки устаревших Django-сессий.                                       |
| `clearsessions-cronjob.yaml` | CronJob для автоматической еженочной очистки сессий.                                    |
| `migrate.yaml`               | Job, запускающая `python manage.py migrate` после деплоя.                               |
