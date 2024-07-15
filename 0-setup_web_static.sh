#!/usr/bin/env bash
# Script to set up web servers for the deployment of web_static

# Install Nginx if it is not already installed
if ! dpkg -l | grep -q nginx; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create the required directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create or update the symbolic link
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content
sudo bash -c 'cat > /etc/nginx/sites-available/default << EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By 230686-web-01;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=dQw4w9WgXcQ;
    }

    error_page 404 /custom_404.html;
    location = /custom_404.html {
        internal;
    }

    location /hbnb_static {
        alias /data/web_static/current;
        autoindex off;
    }
}
EOF'

# Restart Nginx to apply the changes
sudo systemctl restart nginx

# Exit successfully
exit 0
