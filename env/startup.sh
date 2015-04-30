#restart servers
#sudo service nginx restart
#sudo service uwsgi restart
sudo service supervisord start
sudo pip install sqlalchemy-migrate
sudo apt-get install python-dev
sudo apt-get install postgresql
sudo apt-get install libpq-dev
sudo pip install psycopg2
sudo python /app/manage.py runserver


cat "Server is running!!!"
