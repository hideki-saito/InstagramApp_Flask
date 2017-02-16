FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y curl

RUN curl http://nginx.org/keys/nginx_signing.key | apt-key add -
RUN echo "deb http://nginx.org/packages/debian/ jessie nginx" >> /etc/apt/sources.list
RUN echo "deb-src http://nginx.org/packages/debian/ jessie nginx" >> /etc/apt/sources.list
RUN apt-get update

RUN apt-get build-dep -y nginx

WORKDIR /usr/src
RUN apt-get source nginx
RUN ln -s /usr/src/nginx-* /usr/src/nginx

RUN apt-get install -y git

WORKDIR /usr/src
RUN git clone https://github.com/vkholodkov/nginx-upload-module.git

WORKDIR /usr/src/nginx-upload-module
RUN git checkout 2.2

WORKDIR /usr/src/nginx
RUN sed -i.bak "s/--with-ipv6/--add-module=\/usr\/src\/nginx-upload-module --with-ipv6/g" debian/rules
RUN dpkg-buildpackage -uc -b

WORKDIR /

RUN dpkg -i /usr/src/nginx_*.deb

ADD ./cors /etc/nginx/cors
ADD ./nginx.conf /etc/nginx/nginx.conf

ADD ./www-root /www-root

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
