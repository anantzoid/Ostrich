#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/app/")

from app import webapp as application
application.secret_key = 'v9g41jjv%-nx^5*jdd=i*mj^r+blkv8$9!_031ws*axg%!-o-2'
