#!/usr/bin/env bash

gunicorn  ELP_portal.wsgi:application -b 127.0.0.1:8001
