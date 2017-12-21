FROM ubuntu:14.04

MAINTAINER bunseokbot

RUN apt-get update &&\
	apt-get install -y python2.7 python-pip git &&\
	rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Jinmo/AssemblyLearner.git asmlearner

WORKDIR "/asmlearner"

RUN pip install -r requirements.txt
RUN pip install virtualenv virtualenvwrapper
RUN adduser --quiet --disabled-password --shell=/bin/bash --home /home/asmlearner --gecos "" asmlearner
RUN pip install

CMD ["./server.py"]

EXPOSE 80
