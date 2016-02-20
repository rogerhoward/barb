import os, sys

PROJECT_DIR = '/var/www/hookdb'

activate_this = os.path.join('/home/rogerhoward/.virtualenvs/hookdb/bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))
sys.path.append(PROJECT_DIR)

from hook import app as application