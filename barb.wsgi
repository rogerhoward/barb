import os, sys

PROJECT_DIR = '/var/www/barb'

activate_this = os.path.join('/home/rogerhoward/.virtualenvs/barb/bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))
sys.path.append(PROJECT_DIR)

from barb import app as application