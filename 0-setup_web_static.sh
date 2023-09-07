#!/usr/bin/env bash
# this script sets up a webserver for deployment of dir "web_static"

# install nginx
apt-get update -y
apt-get install -y nginx

# create directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# create test index file
echo "<html>
<head>
  <title>Test page</title>
</head>
<body>
  <p> Everything works! </p>
</body>
</html>" >  /data/web_static/releases/test/index.html

# create a symlink
ln -sfn /data/web_static/releases/test/ /data/web_static/current

# give ownership of "data" dir to  user "ubuntu"
chown -R ubuntu:ubuntu /data/

# update nginx config to serve content of
# /data/web_static/current/ to hbnb_static
config_file="/etc/nginx/sites-available/default"
echo "server {
    listen 80 default_server;
    listen [::]:80 default_server;

    add_header X-Served-By \$hostname;

    root   /var/www/html;

    index  index.html index.htm index.nginx-debian.html;

    server_name _;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
    }

    location / {
        # First attempt to serve request as file, then
        # as directory, then fall back to displaying a 404.
        try_files \$uri \$uri/ =404;
    }
}" > $config_file

# restart nginx
service nginx restart
