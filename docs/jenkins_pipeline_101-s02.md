# Jenkins Pipeline 101

두번째 이야기를 시작합니다. 여기서는 실제 Pipeline을 구축해 보도록 하겠습니다.

`새로운 Item` 클릭

1. Enter an item name : notification-service
2. Pipeline 선택 후, OK 버튼 클릭


export JAVA_HOME=/usr/java/jdk1.8.0
/data/jenkins/maven/apache-maven-3.3.9/bin/mvn install:install-file -Dfile=ojdbc6-11.2.0.jar -DgroupId=com.oracle.jdbc -DartifactId=ojdbc6 -Dversion=11.2.0 -Dpackaging=jar
> 