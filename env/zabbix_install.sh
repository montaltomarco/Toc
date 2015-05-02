sudo cp /app/zabbix_config/sources.list /etc/apt/
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C407E17D5F76A32B
sudo apt-get update:w
sudo apt-get install zabbix-server-mysql php5-mysql zabbix-frontend-php
sudo cp /app/zabbix_config/ports.conf /etc/apache2/
sudo cp /etc/app/zabbix_config/zabbix.conf /etc/apache2/sites-available/
sudo cp /app/zabbix_config/zabbix_server.conf /etc/zabbix/
cd /usr/share/zabbix-server-mysql/
sudo gunzip *.gz
sudo mysql --user=root --password=mysql -e "create user 'zabbix@localhost' identified by 'zabbix'; create database zabbix; grant all privileges on zabbix.* to 'zabbix@localhost'; flush privileges; exit;"
sudo mysql --user=root --password=mysql zabbix < schema.sql
sudo mysql --user=root --password=mysql zabbix < images.sql
sudo mysql --user=root --password=mysql zabbix < data.sql
sudo cp /app/zabbix_config/php.ini /etc/php5/apache2/
sudo cp /app/zabbix_config/zabbix.conf.php /etc/zabbix/
sudo cp /usr/share/doc/zabbix-frontend-php/examples/apache.conf /etc/apache2/conf-available/zabbix.conf
sudo a2enconf zabbix.conf
sudo a2enmod alias
sudo service apache2 reload
sudo service apache2 restart
sudo cp /app/zabbix_config/zabbix-server /etc/default/
sudo service zabbix-server start
sudo apt-get update
sudo ls
apt-get install zabbix-agent
sudo cp /app/zabbix_config/zabbix_agentd.conf /etc/zabbix/
sudo service zabbix-agent restart





