base:
    '*':
        - users
        - postfix

    'koosli.org':
        - secure
        - koosli.prod
        - postgres.prod

    'vagrant':
        - secure
        - koosli.vagrant
        - postgres.vagrant
