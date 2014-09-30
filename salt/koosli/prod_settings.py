{% set koosli = pillar.get('koosli') -%}
{% set postgres = pillar.get('postgres') -%}

SECRET_KEY = '{{ koosli.secret_key }}'

SQLALCHEMY_DATABASE_URL = "postgresql://koosli:{{ koosli['db_password'] }}@{{ postgres['db_url'] }}/koosli_rel"
