#!/bin/bash

source .venv/bin/activate

. /home/andrisbremanis/demo-magic.sh
clear

pei "python3 src/main.py image-scraper --search=\"potato\" -s --download-threads=16"
