#!/bin/sh

. ~/.bashrc

pip install -e .

gunicorn --bind 0.0.0.0:5000 manage:app
