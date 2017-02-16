#!/bin/bash -ex

apt-get update && \
apt-get -y install python3 \
                   python3-dev \
                   python3-pip \
                   python3-virtualenv \
                   \
                   libcurl4-openssl-dev \
                   libjpeg-dev \
                   libpng-dev \
                   libpq-dev \
                   \
                   curl \
                   nodejs \
                   npm \
                   openvpn \
                   phantomjs \
                   xvfb
