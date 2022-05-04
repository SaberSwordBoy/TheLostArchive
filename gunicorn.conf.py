# Config for gunicorn webserver

bind = ['0.0.0.0:443', '0.0.0.0:80']
workers = 4


certfile = '/etc/letsencrypt/live/saberfilms.cf/fullchain.pem'
keyfile = '/etc/letsencrypt/live/saberfilms.cf/privkey.pem'
logfile = '/var/log/gunicorn/debug.log'
errorlog =  '/var/log/gunicorn/error.log'
accesslog = "/root/saberfilmsapp/logs/gunicorn.access.log"

loglevel = 'debug'
