# [Kapoor Software Solutions](https://kapoorsoftware.com)


boostit

License: MIT

## How to start this project

### using virtualenv
1. pip install virtualenv
2. virtualenv venv
3. source venv/bin/activate (on linux and mac)
4. source venv/Script/activate (on windows)
5. pip install -r requirement/base.txt
6. pip install -r requirement/local.txt

### using docker
1. cd django-react-boilerplate
2. docker-compose -f local.yml build
3. docker-compose -f local.yml up
if you want to create a superuser you can run 
4. docker-compose -f local.yml run --rm web python manage.py createsuperuser

### using in production
1. run ``` bash cd django-react-boilerplate```
2. changing your domain at compose/production/nginx/nginx.conf replace example.com
3. ``` bash docker-compose -f production.yml build```
4. ``` bash docker-compose -f production.yml up -d```
5. generate ssl for your domain by running if this run successfully by running ``` bash docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d example.org```
6. generate ssl for your domain by running if this run successfully by running ``` bash docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d example.org```
7. run ``` bash docker-compose -f production.yml stop```
8. go to compose/production/nginx/nginx.conf and uncomment the commented part for port 443
9. run ``` bash docker-compose -f production.yml build```
10. run ``` bash docker-compose -f production.yml up -d```
if you want to create a superuser you can run 
11. ``` bash docker-compose -f production.yml run --rm web python manage.py createsuperuser```


### Celery

This app comes with Celery.

To run a celery worker:

``` bash
cd django-react-boilerplate
celery -A kapoorsoftwaresolutions worker -l info
```

To run a celery  beat:

``` bash
cd django-react-boilerplate
celery -A kapoorsoftwaresolutions beat -l info
```

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.
