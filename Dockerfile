FROM java:8 
 
RUN  \
  export DEBIAN_FRONTEND=noninteractive && \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y wget curl maven
 
  RUN mkdir gwt-mvp
 
  WORKDIR /gwt-mvp
 
  CMD ["mvn", "package"]

