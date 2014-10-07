{% set postgresql = pillar.get('postgresql', {}) -%}
{% set version = postgresql.get('version', '9.3') -%}

postgres-server:
  pkgrepo.managed:
    - humanname: PostgreSQL repo
    - name: deb http://apt.postgresql.org/pub/repos/apt/ {{ grains['lsb_distrib_codename'] }}-pgdg main
    - key_url: https://www.postgresql.org/media/keys/ACCC4CF8.asc

  pkg.installed:
    - name: postgresql-{{ version }}
    - require:
      - pkgrepo: postgres-server
    - order: 1

  file.managed:
    - name: /etc/postgresql/{{ version }}/main/pg_hba.conf
    - source: salt://postgres/pg_hba.conf
    - user: postgres
    - group: postgres
    - mode: 640
    - require:
      - pkg: postgres-server

  service.running:
    - name: postgresql
    - require:
      - pkg: postgres-server
    - watch:
      - file: postgres-server
