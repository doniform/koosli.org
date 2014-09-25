# Actual code is deployed by Travis with Fabric, salt merely sets up the server and prepares it
# for deployment

{% set koosli = pillar.get('koosli', {}) %}
{% home = koosli.get('home', '/srv/koosli.org') %}

include:
  - nginx
  - uwsgi

koosli-deps:
  pip.installed:
    - name: virtualenv

  pkg.installed:
    - pkgs:
      - python-dev # needed to compile native code
      - libpq-dev # needed to compile psql bindings


koosli:
  virtualenv.managed:
    - name: {{ home }]/venv
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
    - group: www
    - mode: 640
    - require:
      - virtualenv: koosli
    - watch_in:
      - service: uwsgi


koosli-uwsgi-conf:
  file.managed:
    - name: /opt/apps/koosli.ini
    - source: salt://koosli/uwsgi_conf
    - makedirs: True


koosli-log-dir:
  file.directory:
    - name: /var/log/koosli
    - makedirs: True
    - user: root
    - group: www
    - mode: 775
    - require:
        - user: uwsgi-systemuser


koosli-entry-point:
  file.managed:
    - name: /srv/koosli/koosli_entry_point.py
    - source: salt://koosli/entry_point.py
    - template: jinja


koosli-prod-config:
  file.managed:
    - name: /srv/koosli/prod_config.py
    - source: salt://koosli/config.py
    - user: root
    - group: uwsgi
    - mode: 440
    - template: jinja
    - show_diff: False
    - require:
      - user: uwsgi-systemuser


koosli-postgres:
  postgres_user.present:
    - name: koosli
    - password: "{{ pillar['koosli:db_password'] }}"
    - refresh_password: True

  postgres_database.present:
    - name: koosli_rel
    - owner: koosli
    - require:
      - postgres_user: koosli-postgres


koosli-nginx-site:
  file.managed:
    - name: /etc/nginx/sites-enabled/thusoy.com
    - source: salt://koosli/nginx/thusoy.com
    - template: jinja
    - watch_in:
      - service: nginx
