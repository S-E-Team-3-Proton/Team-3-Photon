#!/bin/bash

# install required packages
pip3 install pygame==2.6.1
pip3 install psycopg2-binary

# check versions
python3 -c "import pygame; print('Pygame version:', pygame.version.ver)"
python3 -c "import psycopg2; print('Psycopg2 version:', psycopg2.__version__)"
