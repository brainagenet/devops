#!/bin/bash
# startJenkins.sh

. ./env.sh

CURDT=`date '+%Y%m%d%H%M%S'`
if [ ! -d ${JENKINS_LOG} ]; then
    mkdir -p ${JENKINS_LOG}
fi

if [ -f ${JENKINS_LOG}/server.log ]; then
    # echo "backup server.log to server.log.${CURDT}"
    mv ${JENKINS_LOG}/server.log ${JENKINS_LOG}/server.log.${CURDT}
fi

nohup ${JAVA_HOME}/bin/java ${JAVA_OPTS} -jar ${JENKINS_BASE}/jenkins-${JENKINS_VER}.war ${JENKINS_OPTS} > ${JENKINS_LOG}/server.log 2>&1 &
