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


# Disable default site
nginx-defaults:
  file.absent:
    - names:
      - /etc/nginx/sites-enabled/default


nginx-sites-enabled:
  file.directory:
    - name: /etc/nginx/sites-enabled
    - user: root
    - group: nginx
    - mode: 755
    - require:
      - file: nginx-conf
      - user: nginx-systemuser
