#restart servers
#sudo service nginx restart
#sudo service uwsgi restart
sudo service supervisord start

# Start a web server that is accessible from anywhere
# python /app/manage.py runserver 0.0.0.0:8080

cat "Server is running!!!"
