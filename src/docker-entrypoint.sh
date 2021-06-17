#!/bin/sh

echo "Start migrations..."

python manage.py migrate --noinput
python manage.py collectstatic --noinput


python manage.py loaddata master_data/group.json
python manage.py loaddata master_data/user.json
python manage.py loaddata master_data/berth.json

exec "$@"