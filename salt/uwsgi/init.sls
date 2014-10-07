uwsgi-systemuser:
  user.present:
    - name: uwsgi
    - fullname: uWSGI worker
    - system: True
    - createhome: False
    - shell: /usr/sbin/nologin


uwsgi-deps:
  pkg.installed:
    - pkgs:
      - python-dev
      - python-pip


uwsgi:
  pip.installed:
    - require:
      - pkg: uwsgi-deps

  file.managed:
    - name: /etc/init/uwsgi.conf
    - source: salt://uwsgi/uwsgi.conf

  service.running:
    - require:
      - file: uwsgi-app-dir
      - file: uwsgi-log-dir
      - pip: uwsgi
      - user: uwsgi-systemuser
    - watch:
      - file: uwsgi


uwsgi-log-dir:
  file.directory:
    - name: /var/log/uwsgi
    - user: root
    - group: uwsgi
    - mode: 775
    - require:
      - user: uwsgi-systemuser


uwsgi-app-dir:
  file.directory:
    - name: /opt/apps
    - user: root
    - group: uwsgi
    - mode: 755
    - require:
      - user: uwsgi-systemuser
