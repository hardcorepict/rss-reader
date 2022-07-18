Simple Rss Reader app
How to start application for local development:

1. Run db and redis:
   sudo docker-compose up

2. Apply migrations:
   python manage.py migrate

3. Start celery worker:
   celery -A rss-reader worker -l INFO

4. Start server:
   python manage.py runserver

5. For running tests:
   pytest

6. Getting test coverage html report:
   pytest --cov=. --cov-report html
