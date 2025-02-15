#!/bin/bash

# install pip
sudo apt-get install python3-pip

# install required packages
python3 -m pip install pygame==2.6.1
python3 -m pip install psycopg2-binary

# check versions
python3 -c "import pygame; print('Pygame version:', pygame.version.ver)"
python3 -c "import psycopg2; print('Psycopg2 version:', psycopg2.__version__)"
