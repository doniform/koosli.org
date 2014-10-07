base:
    '*':
        - users

    'koosli.org':
        - secure
        - koosli.prod
        - postgres.prod

    'vagrant':
        - secure
        - koosli.vagrant
        - postgres.vagrant
