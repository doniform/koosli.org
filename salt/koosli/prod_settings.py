{% set koosli = pillar.get('koosli') -%}

SECRET_KEY = '{{ koosli.secret_key }}'
