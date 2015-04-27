#restart servers
#sudo service nginx restart
#sudo service uwsgi restart
sudo service supervisord start
sudo pip install sqlalchemy-migrate
sudo python /app/manage.py runserver


cat "Server is running!!!"
