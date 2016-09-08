FROM ubuntu/java8:14.04
MAINTAINER MyungSeok, Seo <ms29.seo@gmail.com>

# download latest jenkins war file
RUN mkdir -p /engine/jenkins/app /engine/jenkins/logs /data/jenkins/data \
    && cd /engine/jenkins/app \
    && wget -O jenkins-2.7.3.LTS.war http://mirrors.jenkins-ci.org/war-stable/latest/jenkins.war

COPY *.sh /engine/jenkins/
RUN chmod 700 /engine/jenkins/*.sh

EXPOSE 28080

WORKDIR /engine/jenkins

CMD ['./startJenkins.sh']
