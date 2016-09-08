# Jenkins Pipeline 101

## Install Oracle Java

Oracle JDK를 설치합니다. root 또는 sudo 권한이 있는 사용자로 설치합니다.

```bash
# ---------------------------------------------
# jdk를 설치할 디렉토리를 생성합니다.
$ sudo mkdir -p /usr/java
```

### Java 7

```bash
$ cd /usr/java
$ sudo wget --no-check-certificate --no-cookies \
    --header "Cookie: oraclelicense=accept-securebackup-cookie" \
    http://download.oracle.com/otn-pub/java/jdk/7u80-b15/jdk-7u80-linux-x64.tar.gz
$ sudo tar xvzf jdk-7u80-linux-x64.tar.gz
$ sudo ln -s ./jdk1.7.0_80 jdk1.7.0
$ sudo rm -rf jdk-7u80-linux-x64.tar.gz
$ cd /usr/java/jdk1.7.0/bin
$ ./java -version
```

### Java 8

```bash
$ cd /usr/java
$ sudo wget --no-check-certificate --no-cookies \
    --header "Cookie: oraclelicense=accept-securebackup-cookie" \
    http://download.oracle.com/otn-pub/java/jdk/8u102-b14/jdk-8u102-linux-x64.tar.gz
$ sudo tar xvzf jdk-8u102-linux-x64.tar.gz
$ sudo ln -s ./jdk1.8.0_102 jdk1.8.0
$ sudo rm -rf jdk-8u102-linux-x64.tar.gz
$ cd /usr/java/jdk1.8.0/bin
$ ./java -version
```

## Create Jenkins User

root 또는 sudo 권한이 있는 사용자로 jenkins 계정을 생성합니다.

```bash
# ---------------------------------------------
# 사용자 그룹을 생성합니다.
$ sudo groupadd jenkins

# ---------------------------------------------
# 사용자를 생성합니다.
$ sudo useradd -s /bin/bash -d /home/jenkins -m -g jenkins jenkins

# ---------------------------------------------
# 사용자 비밀번호를 생성합니다.
$ sudo passwd jenkins
  !j3Nk1Ns#79124
```

## create directory structures

jenkins의 작업 디렉토리를 생성합니다.

```bash
# ---------------------------------------------
# as root or sudo user
# /data/jenkins/src 디렉토리를 생성합니다.
$ sudo mkdir -p /data/jenkins/engine /data/jenkins/data /data/jenkins/maven/repo /data/jenkins/ant
$ sudo chown -Rf jenkins:jenkins /data/jenkins
```

## install build tools 

Java에서 주로 많이 쓰이는 Build Tools을 미리 설치하도록 하겠습니다. 여기서는 Apache Ant와 Apache Maven을 설치하도록 하겠습니다.

### Apache Maven

```bash
# ---------------------------------------------
# jenkins 사용자로 전환합니다.
$ sudo su - jenkins

# ---------------------------------------------
# 작업 디렉토리를 생성합니다.
$ cd /data/jenkins/maven

# ---------------------------------------------
# 다운로드 받습니다.
$ wget http://apache.mirror.cdnetworks.com/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz

# ---------------------------------------------
# 압축을 해제합니다.
$ tar xvzf apache-maven-3.3.9-bin.tar.gz
```

설치가 완료되었습니다. 이제 Local Repository Directory를 설정해 줍니다.

```bash
$ cd /data/jenkins/maven/apache-maven-3.3.9/conf
$ vi settings.xml
```

```xml
<?xml version="1.0" encoding="UTF-8"?>

<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 
            http://maven.apache.org/xsd/settings-1.0.0.xsd">
  <!-- localRepository
   | The path to the local repository maven will use to store artifacts.
   |
   | Default: ${user.home}/.m2/repository
  <localRepository>/path/to/local/repo</localRepository>
  -->
  <!-- 위에서 생성한 디렉토리를 지정한다. -->
  <localRepository>/data/jenkins/maven/repo</localRepository>

  <!-- interactiveMode
   | This will determine whether maven prompts you when it needs input. If set to false,
   | maven will use a sensible default value, perhaps based on some other setting, for
   | the parameter in question.
   |
   | Default: true
  <interactiveMode>true</interactiveMode>
  -->

. . .
```

추가적으로 사용자의 Home Directory에 `~/.m2` Directory를 생성하고 settings.xml을 생성한 후, Local Repository Directory를 지정해 줍니다.

> 이렇게 하는 이유는 중복되어 저장되는 것을 막기 위해서 입니다.

```bash
$ mkdir -p ~/.m2
$ cd ~/.m2
$ touch settings.xml
$ vi settings.xml
```

```xml
<?xml version="1.0" encoding="UTF-8"?>

<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 
            http://maven.apache.org/xsd/settings-1.0.0.xsd">
  <localRepository>/data/jenkins/maven/repo</localRepository>
</settings>
```

### Apache Ant

```bash
# ---------------------------------------------
# jenkins 사용자로 전환합니다.
$ sudo su - jenkins

# ---------------------------------------------
# 작업 디렉토리를 생성합니다.
$ cd /data/jenkins/ant

# ---------------------------------------------
# 다운로드 받습니다.
$ wget http://apache.mirror.cdnetworks.com//ant/binaries/apache-ant-1.9.7-bin.tar.gz

# ---------------------------------------------
# 압축을 해제합니다.
$ tar xvzf apache-ant-1.9.7-bin.tar.gz
```

설치가 완료되었습니다. Apache Ant는 별도로 설정할 것이 없습니다.

## install jenkins

[jenkins.io](https://jenkins.io)에서 Jenkins를 [다운로드](http://mirrors.jenkins-ci.org/war-stable/latest/jenkins.war)(2.7.3 LTS Version) 받습니다.

```bash
# jenkins 사용자로 전환합니다.
$ sudo su - jenkins

# 작업 디렉토리로 이동합니다.
$ cd /data/jenkins/engine

# 다운로드 받습니다.
$ wget -O jenkins-2.7.3.LTS.war http://mirrors.jenkins-ci.org/war-stable/latest/jenkins.war
```


## create shellscripts

```bash
$ cd /data/jenkins/engine
$ touch env.sh startJenkins.sh stopJenkins.sh restartJenkins.sh tail.sh && chmod 700 *.sh
```

### env.sh

```bash
$ cd /data/jenkins/engine
$ vi env.sh
```

```bash
#!/bin/bash
# env.sh

export JAVA_HOME="/usr/java/jdk1.8.0"
export JENKINS_HOME="/data/jenkins/data"
export JENKINS_BASE="/data/jenkins/engine"
export JENKINS_LOG="${JENKINS_BASE}/logs"
export JENKINS_VER="2.7.3.LTS"

export JENKINS_PREFIX="/ci"
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
```

### startJenkins.sh

```bash
$ cd /data/jenkins/engine
$ vi startJenkins.sh
```

```bash
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
```

### stopJenkins.sh

```bash
$ cd /data/jenkins/engine
$ vi stopJenkins.sh
```

```bash
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
```

### restartJenkins.sh

```bash
$ cd /data/jenkins/engine
$ vi restartJenkins.sh
```

```bash
#!/bin/bash
# restartJenkins.sh

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

${JAVA_HOME}/bin/java -cp ${JENKINS_HOME}/war/winstone.jar winstone.tools.WinstoneControl reload:${JENKINS_PREFIX} ${JENKINS_OPTS}
```

### tail.sh

```bash
$ cd /data/jenkins/engine
$ vi tail.sh
```

```bash
#!/bin/bash
# tail.sh

export JENKINS_BASE="/data/jenkins/engine"
export JENKINS_LOG="${JENKINS_BASE}/logs"

tail -f ${JENKINS_LOG}/server.log
```

## running jenkins

시험삼아 한번 실행해 봅니다.

```bash
$ /usr/java/jdk1.8.0/bin/java -server -Xverify:none \
    -Dserver=jenkins -DJENKINS_HOME=/data/jenkins/data \
    -jar jenkins-2.7.3.LTS.war \
    --prefix="/jenkins" --httpPort=28080 --controlPort=28005
```

위에서 생성한 ShellScript를 실행해 봅니다.

```bash
$ cd /data/jenkins/engine
$ ./startJenkins.sh ; ./tail.sh
```

```
. . .
Sep 08, 2016 12:47:18 AM org.springframework.context.support.AbstractApplicationContext prepareRefresh
INFO: Refreshing org.springframework.web.context.support.StaticWebApplicationContext@79e0f80f: display name [Root WebApplicationContext]; startup date [Thu Sep 08 00:47:18 KST 2016]; root of context hierarchy
Sep 08, 2016 12:47:18 AM org.springframework.context.support.AbstractApplicationContext obtainFreshBeanFactory
INFO: Bean factory for application context [org.springframework.web.context.support.StaticWebApplicationContext@79e0f80f]: org.springframework.beans.factory.support.DefaultListableBeanFactory@644386d2
Sep 08, 2016 12:47:18 AM org.springframework.beans.factory.support.DefaultListableBeanFactory preInstantiateSingletons
INFO: Pre-instantiating singletons in org.springframework.beans.factory.support.DefaultListableBeanFactory@644386d2: defining beans [authenticationManager]; root of factory hierarchy
Sep 08, 2016 12:47:19 AM org.springframework.context.support.AbstractApplicationContext prepareRefresh
INFO: Refreshing org.springframework.web.context.support.StaticWebApplicationContext@1832cfcf: display name [Root WebApplicationContext]; startup date [Thu Sep 08 00:47:19 KST 2016]; root of context hierarchy
Sep 08, 2016 12:47:19 AM org.springframework.context.support.AbstractApplicationContext obtainFreshBeanFactory
INFO: Bean factory for application context [org.springframework.web.context.support.StaticWebApplicationContext@1832cfcf]: org.springframework.beans.factory.support.DefaultListableBeanFactory@1c385bca
Sep 08, 2016 12:47:19 AM org.springframework.beans.factory.support.DefaultListableBeanFactory preInstantiateSingletons
INFO: Pre-instantiating singletons in org.springframework.beans.factory.support.DefaultListableBeanFactory@1c385bca: defining beans [filter,legacy]; root of factory hierarchy
Sep 08, 2016 12:47:19 AM jenkins.install.SetupWizard init
INFO: 

*************************************************************
*************************************************************
*************************************************************

Jenkins initial setup is required. An admin user has been created and a password generated.
Please use the following password to proceed to installation:

68ac5f48e3a34b8ab5d9186b484043f8

This may also be found at: /data/jenkins/data/secrets/initialAdminPassword

*************************************************************
*************************************************************
*************************************************************

Sep 08, 2016 12:47:24 AM hudson.model.UpdateSite updateData
INFO: Obtained the latest update center data file for UpdateSource default
Sep 08, 2016 12:47:24 AM hudson.WebAppMain$3 run
INFO: Jenkins is fully up and running

```

설치하고 실행이 완료되었습니다.
