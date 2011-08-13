dev:
	python manage.py runserver

init:
	python manage.py syncdb --noinput
	python manage.py populatedb

clean:
	rm -f /tmp/googlecharts
