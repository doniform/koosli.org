{% set koosli = pillar.get('koosli') -%}

from koosli.search_providers import bing

SECRET_KEY = "{{ pillar['KOOSLI_SECRET_KEY'] }}"

SQLALCHEMY_DATABASE_URI = "postgresql://koosli:{{ pillar['KOOSLI_DB_PASSWORD'] }}@{{ salt['config.get']('postgres.host', 'localhost') }}/koosli_rel"

SEARCH_PROVIDERS = {
    'bing': bing.Bing,
}

BING_API_KEY = "{{ pillar['BING_API_KEY'] }}"

LOG_CONF_PATH = '/srv/koosli.org/log_conf.yaml'
