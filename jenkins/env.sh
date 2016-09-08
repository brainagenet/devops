#!/bin/bash
# env.sh

# export JAVA_HOME="/usr/java/jdk1.8.0"
export JENKINS_HOME="/data/jenkins/data"
export JENKINS_BASE="/engine/jenkins/app"
export JENKINS_LOG="${JENKINS_BASE}/logs"
export JENKINS_VER="2.7.3.LTS"

export JENKINS_PREFIX="/jenkins"
export JENKINS_HTTP_PORT=28080
export JENKINS_CTRL_PORT=28005

if [ "x${JENKINS_OPTS}" = "x" ]; then
    JENKINS_OPTS="--prefix=${JENKINS_PREFIX}"
    JENKINS_OPTS="${JENKINS_OPTS} --httpPort=${JENKINS_HTTP_PORT}"
    # JENKINS_OPTS="${JENKINS_OPTS} --ajp13Port=${JENKINS_AJP_PORT}"
    JENKINS_OPTS="${JENKINS_OPTS} --controlPort=${JENKINS_CTRL_PORT}"
fi
export JENKINS_OPTS

if [ "x${JAVA_OPTS}" = "x" ]; then
    JAVA_OPTS="-server"
    JAVA_OPTS="${JAVA_OPTS} -Xverify:none"
    JAVA_OPTS="${JAVA_OPTS} -Dserver=jenkins"

    JAVA_OPTS="${JAVA_OPTS} -DJENKINS_HOME=${JENKINS_HOME}"

    # ----------------------
    # java memery opts
    # ----------------------
    JAVA_OPTS="${JAVA_OPTS} -Djava.awt.headless=true"
    JAVA_OPTS="${JAVA_OPTS} -Xms1024m"
    JAVA_OPTS="${JAVA_OPTS} -Xmx1024m"
    JAVA_OPTS="${JAVA_OPTS} -Xss2m"
    # JAVA_OPTS="${JAVA_OPTS} -XX:PermSize=256m"
    # JAVA_OPTS="${JAVA_OPTS} -XX:MaxPermSize=256m"

    # ----------------------
    # java gc opts
    # ----------------------
    JAVA_OPTS="${JAVA_OPTS} -verbose:gc"
    JAVA_OPTS="${JAVA_OPTS} -Xloggc:${JENKINS_LOG}/gc.log"
    JAVA_OPTS="${JAVA_OPTS} -XX:+PrintGCDetails"
    JAVA_OPTS="${JAVA_OPTS} -XX:+PrintGCTimeStamps"
    JAVA_OPTS="${JAVA_OPTS} -XX:+PrintHeapAtGC"
    JAVA_OPTS="${JAVA_OPTS} -XX:+HeapDumpOnOutOfMemoryError"
    JAVA_OPTS="${JAVA_OPTS} -XX:HeapDumpPath=${JENKINS_LOG}/java_pid.hprof"
fi
export JAVA_OPTS

echo "========================================================"
echo " JAVA_HOME=${JAVA_HOME}"
echo "JENKINS_BASE=${JENKINS_BASE}"
echo "JENKINS_HOME=${JENKINS_HOME}"
echo " JAVA_OPTS=${JAVA_OPTS}"
echo "JENKINS_OPTS=${JENKINS_OPTS}"
echo "========================================================"
