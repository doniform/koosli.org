base:
    '*':
        - users
        - postfix

    'koosli.org':
        - secure
        - koosli.prod
        # Postgres in prod is configured directly in the minion config, with postgres.host,
        # postgres.user = kooslimaster and postgres.pass with the master password

    'vagrant':
        - secure
        - koosli.vagrant
        - postgres.vagrant
