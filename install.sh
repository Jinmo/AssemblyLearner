#!/bin/bash

NSJAIL_DEPS="flex bison protobuf-compiler"
PSQL_DEPS="postgresql postgresql-contrib"
CMARK_GFM_DEPS="cmake"
TRACER_DEPS="gcc-multilib"
INSTALL_DEPS="git python2.7 python-pip"

APT_DEPS="$APT_DEPS $PSQL_DEPS $NSJAIL_DEPS $CMARK_GFM_DEPS $INSTALL_DEPS"

sed -i "s/archive.ubuntu.com/ftp.daumkakao.com/" /etc/apt/sources.list

# Install all required packages
apt-get update &&\
	apt-get install -y $APT_DEPS &&\
	rm -rf /var/lib/apt/lists/*

adduser --quiet --disabled-password --shell=/bin/bash --home /home/asmlearner --gecos "" asmlearner
cd "/home/asmlearner"

git clone --depth 1 --recursive https://github.com/Jinmo/AssemblyLearner.git app
cd "/home/asmlearner/app"

chmod 0777 data

# Install python dependencies
echo "[*] Installing pipenv"
pip install pipenv

# Build modules
echo "[*] Fetching git submodules..."
git submodule update --init --recursive

# Build nsjail
echo "[*] Building nsjail..."
(cd nsjail; make -j5) > /dev/null

# Build cmark-gfm
echo "[*] Building cmark-gfm..."
(cd cmark; mkdir build; cd build; cmake ..; make -j5 install) > /dev/null

# Build asmlearner tracer used when executing assembly
echo "[*] Building asmlearner/bin/tracer..."
(cd asmlearner/bin; make) > /dev/null

# Install python dependencies
pipenv install

su asmlearner -c /scripts/start