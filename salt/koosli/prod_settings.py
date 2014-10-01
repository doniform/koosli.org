{% set koosli = pillar.get('koosli') -%}
{% set postgres = pillar.get('postgres') -%}

from koosli.search_providers import bing

SECRET_KEY = "{{ pillar['KOOSLI_SECRET_KEY'] }}"

SQLALCHEMY_DATABASE_URL = "postgresql://koosli:{{ pillar['KOOSLI_DB_PASSWORD'] }}@{{ postgres['db_url'] }}/koosli_rel"

SEARCH_PROVIDERS = {
    'bing': bing.Bing,
}

BING_API_KEY = "{{ pillar['BING_API_KEY'] }}"
