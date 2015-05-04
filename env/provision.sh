va# update and install essentials
sudo apt-get update
sudo apt-get install build-essential python-dev python-pip curl -y

# install NginX, uWSGI and Redis
sudo apt-get install nginx-full uwsgi uwsgi-plugin-python redis-server -y

# install django
sudo pip install django

# install postgresql
sudo apt-get install libmysqlclient-dev python-mysqldb -y
sudo pip install mysql-python
sudo apt-get install libpq-dev -y
sudo pip install psycopg2
sudo apt-get install postgresql -y

sudo cp /vagrant/conf/pg_hba.conf /etc/postgresql/*/main/pg_hba.conf
sudo cp /vagrant/conf/postgresql.conf /etc/postgresql/*/main/postgresql.conf
sudo service postgresql restart
sudo createdb db_data -U postgres
sudo su - postgres -c "psql -U postgres -d db_data -c \"alter user postgres with password 'postgres';\""
sudo service postgresql restart

export PYTHONPATH=/app/toc
echo 'export PYTHONPATH=/app/toc/' >> ~/.bashrc

#cp run script to home folder
sudo cp /vagrant/run.sh /home/vagrant
echo "That's all folks!"