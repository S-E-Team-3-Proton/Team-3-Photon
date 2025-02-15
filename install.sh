#!/bin/bash

# install pip
sudo apt install python3-pip

# install required packages
python3 -m pip3 install psycopg2-binary
python3 -m pip3 install pygame==2.6.1

# check versions
python3 -c "import psycopg2; print('Psycopg2 version:', psycopg2.__version__)"
python3 -c "import pygame; print('Pygame version:', pygame.version.ver)"
