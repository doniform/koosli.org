# Actual code is deployed by Travis with Fabric, salt merely sets up the server and prepares it
# for deployment

{% set koosli = pillar.get('koosli', {}) %}
{% set home = '/srv/koosli.org' %}

include:
  - nginx
  - uwsgi
  - postgres.client

koosli-deps:
  pip.installed:
    - name: virtualenv

  pkg.installed:
    - pkgs:
      - python-dev # needed to compile native code
      - libpq-dev # needed to compile postgres bindings


koosli:
  virtualenv.managed:
    - name: {{ home }}/venv
    - requirements: salt://koosli/prod-requirements.txt
    - require:
      - pip: koosli-deps
      - pkg: koosli-deps

  file.managed:
    - name: {{ home }}/prod_settings.py
    - source: salt://koosli/prod_settings.py
    - template: jinja
    - show_diff: False
    - user: root
    - group: uwsgi
    - mode: 440
    - require:
      - virtualenv: koosli
      - user: uwsgi-systemuser
    - watch_in:
      - service: uwsgi


koosli-uwsgi-conf:
  file.managed:
    - name: /opt/apps/koosli.ini
    - source: salt://koosli/uwsgi-config.ini
    - makedirs: True


koosli-static-dir:
  file.directory:
    - name: {{ home }}/static
    - mode: 755


koosli-log-dir:
  file.directory:
    - name: /var/log/koosli
    - makedirs: True
    - user: root
    - group: uwsgi
    - mode: 775
    - require:
        - user: uwsgi-systemuser


koosli-entry-point:
  file.managed:
    - name: {{ home }}/koosli_entry_point.py
    - source: salt://koosli/entry_point.py
    - template: jinja


koosli-postgres:
  postgres_user.present:
    - name: koosli
    - password: "{{ pillar['KOOSLI_DB_PASSWORD'] }}"
    - refresh_password: True
    - require:
        - pkg: postgres-client

  postgres_database.present:
    - name: koosli_rel
    - owner: koosli
    - require:
      - postgres_user: koosli-postgres


koosli-nginx-site:
  file.managed:
    - name: /etc/nginx/sites-enabled/koosli.org
    - source: salt://koosli/nginx/koosli.org
    - template: jinja
    - watch_in:
      - service: nginx


koosli-nginx-www-certificate:
  file.managed:
    - name: /etc/nginx/ssl/www.koosli.org.crt
    - contents_pillar: koosli:nginx_cert
    - require:
        - file: nginx-certificates-dir
    - watch_in:
      - service: nginx


koosli-nginx-www-key:
  file.managed:
    - name: /etc/nginx/private/www.koosli.org.key
    - contents_pillar: KOOSLI_NGINX_PRIVATE_KEY
    - user: root
    - group: nginx
    - show_diff: False
    - mode: 640
    - require:
      - user: nginx-systemuser
      - file: nginx-private-dir
    - watch_in:
      - service: nginx
