# update and install essentials
sudo apt-get update
sudo apt-get install build-essential python-dev python-pip curl -y

# install NginX, uWSGI and Redis
sudo apt-get install nginx-full uwsgi uwsgi-plugin-python redis-server -y

# install django
sudo pip install django
<<<<<<< HEAD
sudo pip install sqlalchemy-migrate
sudo apt-get install python-dev
sudo apt-get install postgresql


sudo apt-get install libpq-dev
sudo pip install psycopg2
=======

# install postgresql
sudo apt-get install libmysqlclient-dev python-mysqldb -y
sudo pip install mysql-python
sudo apt-get install libpq-dev -y
sudo pip install psycopg2
sudo apt-get install postgresql -y

sudo cp /vagrant/conf/pg_hba.conf /etc/postgresql/*/main/pg_hba.conf
sudo service postgresql restart
sudo createdb db_data -U postgres
sudo su - postgres -c "psql -U postgres -d db_data -c \"alter user postgres with password 'postgres';\""
sudo service postgresql restart
>>>>>>> 810b4e7be0fe39e1e9718c48bf2171d2d2b82bb1

export PYTHONPATH=/app/toc
echo 'export PYTHONPATH=/app/toc/' >> ~/.bashrc
sudo easy_install supervisor
sudo cp /vagrant/conf/supervisord.sh /etc/init.d/supervisord
sudo sed -i 's/\r//g' /etc/init.d/supervisord
sudo chmod +x /etc/init.d/supervisord
sudo update-rc.d supervisord defaults

# configure uWSGI
touch /tmp/uwsgi.sock
sudo chown www-data /tmp/uwsgi.sock
sudo ln -s /vagrant/conf/app.uwsgi /etc/uwsgi/apps-available/app.ini
sudo ln -s /etc/uwsgi/apps-available/app.ini /etc/uwsgi/apps-enabled/app.ini

# configure NginX
sudo rm /etc/nginx/sites-enabled/default
sudo rm /etc/nginx/sites-available/default
sudo ln -s /vagrant/conf/app.nginx /etc/nginx/sites-available/app
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/app

# configure Redis
# sudo cp /vagrant/conf/app.redis /etc/redis/redis.conf
# sudo ln -s /vagrant/conf/app.redis /etc/redis/redis.conf

# install lynx browser for testing
sudo apt-get install lynx

#install Werkzeug
sudo pip install Werkzeug

<<<<<<< HEAD
=======
#cp run script to home folder
sudo cp /vagrant/run.sh /home/vagrant
>>>>>>> 810b4e7be0fe39e1e9718c48bf2171d2d2b82bb1
echo "That's all folks!"