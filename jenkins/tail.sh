#!/bin/bash
# tail.sh

export JENKINS_BASE="/data/jenkins/engine"
export JENKINS_LOG="${JENKINS_BASE}/logs"

tail -f ${JENKINS_LOG}/server.log
