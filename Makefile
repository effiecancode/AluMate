serve:
	python3 manage.py runserver

migrations:
	python3 manage.py makemigrations
	python3 manage.py migrate

superuser:
	python3 manage.py createsuperuser

requirements:
	python3 -m pip install -r requirements.txt

test:
	python3 manage.py test

flush:
	python3 manage.py flush

rmmigrations:
	rm -rfv ./*/migrations/!(__init__.py)
	rm -rfv __pycache__

syncdb:
	python3 manage.py migrate --run-syncdb

showmigrations:
	python3 manage.py showmigrations

install:
	python3 -m pip install -r requirements.txt

heroku_migrations:
	heroku run python manage.py makemigrations
	heroku run python manage.py migrate

heroku_superuser:
	heroku run python manage.py createsuperuser

activate:
	source env/bin/activate

loadPFScholarCodesToDb:
	python manage.py load_data elp_test_data.xlsx

precommit:
	pre-commit install
	pre-commit run --all-files

uploadToAWSDbLocally:
	\copy user_module_userdata FROM '/home/john/Downloads/elp_test_data.csv' WITH (FORMAT CSV, HEADER);
