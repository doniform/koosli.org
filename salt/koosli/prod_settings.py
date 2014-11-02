{% set koosli = pillar.get('koosli') -%}
{% set postgres_host = salt['config.get']('postgres.host', 'localhost') -%}

from koosli.search_providers import bing

SECRET_KEY = "{{ pillar['KOOSLI_SECRET_KEY'] }}"

SQLALCHEMY_DATABASE_URI = "postgresql://koosli:{{ pillar['KOOSLI_DB_PASSWORD'] }}@{{ postgres_host }}/koosli_rel"

SEARCH_PROVIDERS = {
    'bing': bing.Bing,
}

BING_API_KEY = "{{ pillar['BING_API_KEY'] }}"

YAHOO_CONSUMER_SECRET = "{{ pillar['YAHOO_CONSUMER_SECRET'] }}"

LOG_CONF_PATH = '/srv/koosli.org/log_conf.yaml'

SPLASH_REGISTRATION = True

SESSION_COOKIE_SECURE = True
