FROM httpd:2.4

RUN apt-get update && apt-get upgrade -y

COPY ./www/ /usr/local/apache2/htdocs/
COPY ./httpd-container.conf /usr/local/apache2/conf/httpd.conf
