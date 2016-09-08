#!/bin/bash
# tail.sh

export JENKINS_BASE="/engine/jenkins"
export JENKINS_LOG="${JENKINS_BASE}/logs"

tail -f ${JENKINS_LOG}/server.log
