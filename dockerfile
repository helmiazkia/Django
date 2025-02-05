FROM php:8.0-fpm
WORKDIR /var/www/html
RUN docker-php-ext-install mysqli
FROM python:3.11
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
CMD ["sleep", "infinity"]