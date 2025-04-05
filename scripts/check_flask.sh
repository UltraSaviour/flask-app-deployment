#!/bin/bash

if ! pgrep -f "app.py" > /dev/null
then
    echo "$(date): Flask app not running. Restarting..." >> /var/log/flask_monitor.log
    cd /root/flask_app
    source venv/bin/activate
    nohup python app.py &
else
    echo "$(date): Flask app is running." >> /var/log/flask_monitor.log
fi
