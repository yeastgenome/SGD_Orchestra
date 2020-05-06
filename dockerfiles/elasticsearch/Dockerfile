# Dockerfile containing OS configurations and Elasticsearch installation
# author: felixgondwe

# creates/ a layer from ubuntu@16.04
FROM ubuntu:16.04
LABEL author="Felix Gondwe, gondwefelix8@gmail.com" 
LABEL description="image for elasticsearch 7.5"
LABEL version="20.1.0"

# Update Ubuntu Software respository
# install applications that we need to run elasticsearch successful
# for elasticsearch we will be downloading it over https sp we need apt-transport-https
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y curl \
    wget \
    make \
    gcc \
    ca-certificates \
    software-properties-common \
    apt-transport-https \
    gzip \
    iputils-ping \
    iproute2 \
    apt-utils \
    net-tools

# elasticsearch needs to run with different user than root
# create user to run elasticsearch
RUN groupadd -g 1000 elasticsearch && useradd elasticsearch -u 1000 -g 1000

# install certificate and elasticsearch
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch |  apt-key add -
RUN add-apt-repository "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-7.5.list

RUN apt-get update
# RUN apt-get install -y elasticsearch
RUN apt-get install -y --no-install-recommends elasticsearch

#add elasticsearch to path
ENV PATH=$PATH:/usr/share/elasticsearch/bin
# setup working directory
WORKDIR /usr/share/elasticsearch

# user permissions
USER root
# create data folder
RUN mkdir data
# modify permissions
RUN usermod -g root elasticsearch
RUN chown -R 1000:1000 /usr/share/elasticsearch
RUN chown -R 1000:1000 /etc
# set user to elasticsearch since it no longer runs as root
USER elasticsearch

# start elasticsearch
CMD ["elasticsearch"]

# expose ports to establish connection between the container and the outside world
EXPOSE 9200 9300


