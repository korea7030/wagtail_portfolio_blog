#!/bin/bash

NAME="wagtail_portfolio_blog"                              #Name of the application (*)
DJANGODIR=/app/             # Django project directory (*)
SOCKFILE=/run/gunicorn/gunicorn.sock        # we will communicate using this unix socket (*)
USER=root                                        # the user to run as (*)
GROUP=root                                     # the group to run as (*)
NUM_WORKERS=4                                     # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=wagtail_portfolio_blog.settings.production             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=wagtail_portfolio_blog.wsgi                     # WSGI module name (*)

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
#export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE