# Actual code deployed by Travis and fabric, just set up the virtualenv and the directories needed

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


koosli-nginx-site:
  file.managed:
    - name: /etc/nginx/sites-enabled/koosli.org
    - source: salt://koosli/koosli-nginx-site
    - require:
      - pkg: nginx
