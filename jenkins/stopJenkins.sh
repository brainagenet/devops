#!/bin/bash
# stopJenkins.sh 

. ./env.sh

unset JAVA_OPTS
unset JENKINS_OPTS

if [ "x${JENKINS_OPTS}" = "x" ]; then
    # ----------------------
    # jenkins opts
    # ----------------------
    JENKINS_OPTS="--host=localhost"
    JENKINS_OPTS="${JENKINS_OPTS} --port=${JENKINS_CTRL_PORT}"
fi
export JENKINS_OPTS

${JAVA_HOME}/bin/java -cp ${JENKINS_HOME}/war/winstone.jar winstone.tools.WinstoneControl shutdown ${JENKINS_OPTS}