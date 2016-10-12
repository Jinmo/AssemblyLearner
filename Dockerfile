FROM ubuntu:14.04

MAINTAINER bunseokbot

RUN apt-get update &&\
	apt-get install -y python3.4 python3-pip git &&\
	rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Jinmo/AssemblyLearner.git

WORKDIR "/AssemblyLearner"

RUN pip3 install -r requirements.txt

CMD ["python3", "server.py"]

EXPOSE 3333
