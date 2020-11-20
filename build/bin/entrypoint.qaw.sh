#!/bin/sh

. ~/.bashrc

pip install -e .
pip install -r requirements.txt

gunicorn --bind 0.0.0.0:5000 manage:app
