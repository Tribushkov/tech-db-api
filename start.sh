#!/bin/bash
gunicorn -c gunicorn_conf.py wsgi:app
echo
