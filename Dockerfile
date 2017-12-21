FROM ubuntu:16.04

MAINTAINER Jinmo

ADD https://raw.githubusercontent.com/Jinmo/AssemblyLearner/master/install.sh /install.sh
ADD https://raw.githubusercontent.com/Jinmo/AssemblyLearner/master/scripts/start /scripts/start
ADD https://raw.githubusercontent.com/Jinmo/AssemblyLearner/master/scripts/stop /scripts/stop
RUN chmod +x /install.sh /scripts/start /scripts/stop
RUN /install.sh

CMD ["./server.py"]

EXPOSE 80
