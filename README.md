# cyclone presentation + slide remote control

    deck is a bundled slidedeck and remote control to show up cyclone capabilities
    gleicon - 2013

## About

This file has been created automatically by cyclone for deck.
It contains the following:

- ``start.sh``: simple shell script to start the development server
- ``deck.conf``: configuration file for the web server
- ``deck/``: web server code
- ``frontend/``: static files, templates and locales
- ``scripts/``: debian init scripts and other useful scripts

### nginx

Set server_name, access_log and proxy_pass to the proper settings on your system

server {
        listen   80;
        server_name  s.chu.pe;

        access_log  /var/log/nginx/s.chu.pe.access.log;

        location / {

                root   /var/www/s.chu.pe/;
                index  index.html index.htm;
                proxy_pass                  http://127.0.0.1:11000;
                proxy_redirect              off;

                proxy_set_header            Host            $host;
                proxy_set_header            X-Real-IP       $remote_addr;
                proxy_set_header            X-Forwarded-For $remote_addr;

                proxy_buffering off;
                
                client_max_body_size        128k;
                client_body_buffer_size     128k;

                proxy_connect_timeout       30;
                proxy_send_timeout          30;
                proxy_read_timeout          30;

                proxy_buffer_size           4k;
                proxy_buffers               4 32k;
                proxy_busy_buffers_size     64k;
                proxy_temp_file_write_size  64k;

        }
}

### supervisord

at /etc/supervisord/conf.d/your_app.conf

[program:your_app]
command=/bin/bash /opt/deck/start.sh
redirect_stderr=true
stdout_logfile=/var/log/your_app.log
stdout_logfile_maxbytes=100MB


### Running

For development and testing:

    twistd -n cyclone --help
    twistd -n cyclone -r deck.web.Application [--help]

    or just run ./start.sh


For production:

    twistd cyclone \
            --logfile=/var/log/deck.log \
            --pidfile=/var/run/deck.pid \
            -r deck.web.Application

    or check scripts/debian-init.d and scripts/debian-multicore-init.d


## Dependencies

    Python, Twisted, Cyclone, Redis

## Credits

- [cyclone](http://github.com/fiorix/cyclone) web server.
