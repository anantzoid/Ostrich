sudo rsync -a --exclude='app/static/js/node_modules'  /home/ubuntu/app /var/www
sudo service apache2 restart
slackcat "Deployed!" -n "millenium-falcon"
