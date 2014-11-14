postfix:
  pkg:
    - installed

  file.managed:
    - name: /etc/postfix/main.cf
    - source: salt://postfix/main.cf
    - template: jinja

  service.running:
    - enable: True
    - require:
      - pkg: postfix
    - watch:
      - file: postfix


# Make sure nothing is sent out in dev mode
{% if grains['id'] == 'vagrant' %}
local-redirect:
  file.managed:
    - name: /etc/postfix/canonical-redirect
    - contents: /^.*$/ root
    - watch_in:
      - service: postfix
{% endif %}
