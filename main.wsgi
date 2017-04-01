import sys
from flask_sitemap import Sitemap
sys.path.insert(0, '/var/www/html/iveypage')

from main import app as application

ext = Sitemap(app=application)
