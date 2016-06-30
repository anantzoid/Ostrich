cd /home/ubuntu/app/app/static/js/ && npm run pack
sudo rsync -a --exclude='app/static/js/node_modules'  /home/ubuntu/app /var/www
sudo service apache2 restart
sudo supervisorctl restart node
slackcat "Deployed!" -n "millenium-falcon"
