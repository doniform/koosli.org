{% set nginx = pillar.get('nginx', {}) -%}
{% set version = nginx.get('version', '1.7.5') -%}
{% set checksum = nginx.get('checksum', 'sha1=432303cf9694eedb56a5a91d86536beb604d766b') -%}
{% set home = nginx.get('home', '/usr/local/nginx') -%}
{% set source = nginx.get('source_root', '/usr/local/src') -%}

{% set nginx_package = source + '/nginx-' + version + '.tar.gz' -%}
{% set nginx_home     = home + "/nginx-" + version -%}
{% set nginx_modules_dir = source + "/nginx-modules" -%}


get-nginx:
  pkg.installed:
    - names:
      - libpcre3-dev
      - build-essential
      - libssl-dev
      - libpam0g-dev

  file.managed:
    - name: {{ nginx_package }}
    - source: http://nginx.org/download/nginx-{{ version }}.tar.gz
    - source_hash: {{ checksum }}

  cmd.wait:
    - cwd: {{ source }}
    - name: tar -zxf {{ nginx_package }} -C {{ home }}
    - require:
      - pkg: get-nginx
      - file: {{ home }}
    - watch:
      - file: get-nginx

get-ngx_devel_kit:
  file.managed:
    - name: {{ source }}/ngx_devel_kit.tar.gz
    - source: https://github.com/simpl/ngx_devel_kit/archive/v0.2.18.tar.gz
    - source_hash: sha1=e21ba642f26047661ada678b21eef001ee2121d8

  cmd.wait:
    - cwd: {{ nginx_home }}
    - name: tar -zxf {{ source }}/ngx_devel_kit.tar.gz -C {{ source }}
    - require:
      - file: nginx-home
    - watch:
      - file: get-ngx_devel_kit


get-lua-nginx-module:
  file.managed:
    - name: {{ source }}/lua-nginx-module.tar.gz
    - source: https://github.com/chaoslawful/lua-nginx-module/archive/v0.8.3rc1.tar.gz
    - source_hash: sha1=49b2fa946517fb2e9b26185d418570e98ff5ff51

  cmd.wait:
    - cwd: {{ nginx_home }}
    - name: tar -zxf {{ source }}/lua-nginx-module.tar.gz -C {{ source }}
    - require:
      - file: nginx-home
    - watch:
      - file: get-lua-nginx-module


get-pam-auth-module:
    file.managed:
        - name: {{ source }}/ngx_http_auth_pam_module.tar.gz
        - source: http://web.iti.upv.es/~sto/nginx/ngx_http_auth_pam_module-1.3.tar.gz
        - source_hash: sha1=4c5f64243b8bdeede5dadbf74cc7ab5af04dbb46

    cmd.wait:
        - name: tar xf ngx_http_auth_pam_module.tar.gz
        - cwd: {{ source }}
        - require:
            - file: nginx-home
        - watch:
            - file: get-pam-auth-module


nginx-home:
  file.directory:
    - name: {{ home }}
    - user: nginx
    - group: nginx
    - makedirs: True
    - mode: 0755
    - require:
      - user: nginx-systemuser


nginx:
  cmd.wait:
    - cwd: {{ nginx_home }}
    - name: ./configure --conf-path=/etc/nginx/nginx.conf
            --add-module={{ source }}/ngx_http_auth_pam_module-1.3
            --sbin-path=/usr/sbin/nginx
            --user=nginx
            --group=nginx
            --prefix=/usr/local/nginx
            --error-log-path=/var/log/nginx/error.log
            --pid-path=/var/run/nginx.pid
            --lock-path=/var/lock/nginx.lock
            --http-log-path=/var/log/nginx/access.log
            --with-http_dav_module
            --http-client-body-temp-path={{ home }}/body
            --http-proxy-temp-path={{ home }}/proxy
            --with-http_stub_status_module
            --http-fastcgi-temp-path={{ home }}/fastcgi
            --with-debug
            --with-http_ssl_module &&
            make -j2 && make install
    - watch:
      - cmd: get-nginx
    - require:
      - cmd: get-nginx
      - cmd: get-lua-nginx-module
      - cmd: get-ngx_devel_kit
      - cmd: get-pam-auth-module
    - require_in:
      - service: nginx

  file.managed:
    - name: /etc/init/nginx.conf
    - source: salt://nginx/nginx-upstart
    - user: root
    - group: root
    - mode: 440

  service.running:
    - enable: True
    - require:
      - cmd: nginx
      - file: {{ home }}
      - file: nginx-certificates-dir
      - file: nginx-defaults
      - file: nginx-private-dir
      - file: nginx-sites-enabled
    - watch:
      - file: nginx
      - file: nginx-conf
