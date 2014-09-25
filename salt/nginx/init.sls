{% set nginx = pillar.get('nginx', {}) %}


nginx-systemuser:
  user.present:
    - name: nginx
    - fullname: nginx worker
    - system: True
    - createhome: False
    - shell: /usr/sbin/nologin


include:
  - nginx.source


nginx-conf:
  file.managed:
    - name: /etc/nginx/nginx.conf
    - source: salt://nginx/nginx.conf
    - mode: 640
    - user: root
    - group: nginx
    - require:
      - cmd: nginx
    - watch_in:
      - service: nginx


nginx-certificates-dir:
  file.directory:
    - name: /etc/nginx/ssl
    - user: root
    - group: nginx
    - file_mode: 755
    - require:
      - file: nginx-conf
      - user: nginx-systemuser


nginx-private-dir:
  file.directory:
    - name: /etc/nginx/private
    - user: root
    - group: nginx
    - mode: 750
    - require:
      - file: nginx-conf
      - user: nginx-systemuser


# Disable defaults
nginx-defaults:
  file.absent:
    - names:
      - /etc/nginx/sites-enabled/default
    {% for default_file in ['fastcgi.conf', 'fastcgi_params', 'mime.types', 'nginx.conf',
      'scgi_params', 'uwsgi_params'] %}
      - /etc/nginx/{{ default_file }}.default
    {% endfor %}


nginx-www-certificate:
  file.managed:
    - name: /etc/nginx/ssl/www.koosli.org.crt
    - source: salt://nginx/ssl/www.koosli.org.crt
    - require:
        - file: nginx-certificates-dir
    - watch_in:
      - service: nginx


nginx-www-key:
  file.managed:
    - name: /etc/nginx/private/www.koosli.org.key
    - contents_pillar: NGINX_WWW_PRIVATE_KEY
    - user: root
    - group: nginx
    - show_diff: False
    - mode: 640
    - require:
      - user: nginx-systemuser
      - file: nginx-private-dir
    - watch_in:
      - service: nginx


nginx-sites-enabled:
  file.directory:
    - name: /etc/nginx/sites-enabled
    - user: root
    - group: nginx
    - mode: 755
    - require:
      - file: nginx-conf
      - user: nginx-systemuser
