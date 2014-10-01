{% set koosli = pillar.get('koosli') -%}
{% set postgres = pillar.get('postgres') -%}

SECRET_KEY = "{{ pillar['KOOSLI_SECRET_KEY'] }}"

SQLALCHEMY_DATABASE_URL = "postgresql://koosli:{{ pillar['KOOSLI_DB_PASSWORD'] }}@{{ postgres['db_url'] }}/koosli_rel"
