base:
    '*':
        - users

    'koosli.org':
        - secure
        - koosli.prod
        - postgres.prod

    'vagrant':
        - koosli.vagrant
        - postgres.vagrant
