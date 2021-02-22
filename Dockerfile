FROM nginx:alpine
COPY dist /usr/share/nginx/html

# Nginx configuration files
COPY conf/default.conf /etc/nginx/conf.d/default.conf
COPY conf/auth/htpasswd /etc/nginx/auth/htpasswd


EXPOSE 80
