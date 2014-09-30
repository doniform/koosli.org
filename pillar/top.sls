base:
    '*':
        - secure
        - users

    'koosli.org':
        - postgres.prod

    'vagrant':
        - koosli.vagrant
        - postgres.vagrant
