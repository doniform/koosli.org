base:
    '*':
        - users

    'koosli.org':
        - secure
        - postgres.prod

    'vagrant':
        - koosli.vagrant
        - postgres.vagrant
