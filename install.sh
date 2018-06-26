#!/bin/bash

NSJAIL_DEPS="flex bison protobuf-compiler"
PSQL_DEPS="postgresql postgresql-contrib"
CMARK_GFM_DEPS="cmake"
TRACER_DEPS="gcc-multilib"
INSTALL_DEPS="git python2.7 python-pip"
APT_DEPS="$APT_DEPS $PSQL_DEPS $NSJAIL_DEPS $CMARK_GFM_DEPS $INSTALL_DEPS"

# sed -i "s/archive.ubuntu.com/ftp.daumkakao.com/" /etc/apt/sources.list

# Install all required packages
# apt-get update

sudo apt-get -f install -y$APT_DEPS
# rm -rf /var/lib/apt/lists/*

sudo -u postgres psql -U postgres <<EOF
CREATE DATABASE asmlearner ENCODING utf8;
CREATE ROLE asmlearner LOGIN ENCRYPTED PASSWORD 'dydgnldydgnljinmo123x';
EOF

python -c "import re,os;print(re.sub(r'\\$\{([^}]+)\}', lambda x: eval(x.group(1)), open('asmlearner/secrets.local.py', 'rb').read()).replace(' = ', '='))" > /tmp/secrets.py
mv /tmp/secrets.py asmlearner/secrets.py

# You know what?! It's even compatible with bash!!
. asmlearner/secrets.py

exit

adduser --quiet --disabled-password --shell=/bin/bash --home /home/asmlearner --gecos "" asmlearner
rm -rf /home/asmlearner/*
cd "/home/asmlearner"

su asmlearner -c "$(cat <<EOF
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
pipenv shell "bash scripts/start"
EOF
)"