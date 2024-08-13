# NGINX config

/etc/nginx/conf.d/ai.conf

```
proxy_cache_path /tmp/nginx/cache levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m use_temp_path=off;

server {
    listen       127.0.0.1:5052;
    server_name  localhost;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/w10137/work/AI/preprod/tmp/sock_app.sock;
        proxy_cache my_cache;
        proxy_cache_valid 200 1h;
        proxy_cache_valid 404 1m;
        uwsgi_read_timeout 3600;
        uwsgi_send_timeout 3600;
        uwsgi_connect_timeout 3600;

        #root   /usr/share/nginx/html;
        #index  index.html index.htm;
    }


    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
    error_log /home/w10137/work/AI/preprod/tmp/nginx_error.log;
}
```
