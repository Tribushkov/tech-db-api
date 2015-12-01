#!/bin/bash
gunicorn -c conf/gunicorn_conf.py wsgi:app
echo
