{% set koosli = pillar.get('koosli') -%}
{% set postgres_host = salt['config.get']('postgres.host', 'localhost') -%}
{% set verify_ssl = salt['config.get']('postgres.verify_ssl', True) -%}

SECRET_KEY = "{{ pillar['KOOSLI_SECRET_KEY'] }}"

SQLALCHEMY_DATABASE_URI = "postgresql://koosli:{{ pillar['KOOSLI_DB_PASSWORD'] }}@{{ postgres_host }}/koosli_rel{% if verify_ssl %}?sslrootcert=/srv/koosli.org/rds-root.crt&sslmode=verify-full{% endif %}"

BING_API_KEY = "{{ pillar['BING_API_KEY'] }}"

YAHOO_CONSUMER_SECRET = "{{ pillar['YAHOO_CONSUMER_SECRET'] }}"

LOG_CONF_PATH = '/srv/koosli.org/log_conf.yaml'

SPLASH_REGISTRATION = True

SESSION_COOKIE_SECURE = True
