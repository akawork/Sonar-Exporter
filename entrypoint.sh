#!/usr/bin/env bash

if [ $SONAR_SERVER ]; then
    sed -i "s~http://sonar_server~$SONAR_SERVER~g" config.ini
fi

if [ $SONAR_USERNAME ]; then
    sed -i "s/username/$SONAR_USERNAME/g" config.ini
fi

if [ $SONAR_PASSWORD ]; then
    sed -i "s/password/$SONAR_PASSWORD/g" config.ini
fi

# Run exporter
.local/bin/uwsgi --http 0.0.0.0:${SONAR_EXPORTER_PORT:-9119} --wsgi-file main.py --callable app
