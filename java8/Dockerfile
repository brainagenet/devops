FROM ubuntu:14.04
MAINTAINER MyungSeok, Seo <ms29.seo@gmail.com>

# install basic packages
RUN apt-get update --quiet --quiet \
    && apt-get install --quiet --quiet --no-install-recommends wget \
    && rm -rf /var/lib/apt/lists/*

# install java 8
RUN mkdir -p /usr/java
COPY jdk-8u102-linux-x64.tar.gz /usr/java/
RUN cd /usr/java \
    && tar xvzf jdk-8u102-linux-x64.tar.gz \
    && rm -rf jdk-8u102-linux-x64.tar.gz \
    && ln -sv /usr/java/jdk1.8.0_102 jdk1.8.0

ENV JAVA_HOME=/usr/java/jdk1.8.0
