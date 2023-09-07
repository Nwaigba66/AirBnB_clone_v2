# puppet manifest to setup servers for deployment

package { 'nginx':
  ensure => installed,
}

-> file { '/data':
  ensure  => 'directory'
}

-> file { '/data/web_static':
  ensure => 'directory'
}

-> file { '/data/web_static/releases':
  ensure => 'directory'
}

-> file { '/data/web_static/releases/test':
  ensure => 'directory'
}

-> file { '/data/web_static/shared':
  ensure => 'directory'
}

-> file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html>
<head>
  <title>Test page</title>
</head>
<body>
  <p> Everything works! </p>
</body>
</html>',
}

-> file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
  force  => true,
}

-> exec { 'set_owner':
  command => '/usr/bin/chown -R ubuntu:ubuntu /data/',
}

-> file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "Hello World!\n"
}

-> file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n"
}

-> file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => "server {
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
        try_files \$uri \$uri/ =404;
    }
}",
}

-> service { 'nginx':
  ensure => running,
  enable => true,
}
