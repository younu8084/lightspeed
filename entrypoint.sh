sudo yum install docker
sudo service docker start
sudo curl -L "https://github.com/docker/compose/releases/version/dowload/1.27.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker volume create postgres-volume
docker-compose up