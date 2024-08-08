release: python manage.py migrate
web: gunicorn point_market_backend.wsgi --workers 4 --threads 2
clock: python manage.py pull_zellular
clock: python manage.py run_market
clock: python manage.py scan
