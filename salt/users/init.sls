inputrc:
    file.append:
        - name: /etc/inputrc
        - text: set completion-ignore-case on


{% for name, user in pillar.get('users', {}).items() %}

{% for group in user.get('groups', []) %}
{{ name }}_{{ group }}_group:
    group.present:
        - name: {{ group }}
{% endfor %}

{{ name }}_user:
    user.present:
        - name: {{ name }}
        - shell: {{ user.get('shell', '/bin/bash') }}
        {% if 'password_pillar' in user -%}
        - password: {{ pillar[user['password_pillar']] }}
        {% endif -%}
        - gid_from_name: True
        {% if 'fullname' in user %}
        - fullname: {{ user['fullname'] }}
        {% endif -%}
        - groups:
            {% for group in user.get('groups', []) -%}
            - {{ group }}
            {% endfor %}
        {% if user.get('groups') %}
        - require:
            {% for group in user.get('groups', []) -%}
            - group: {{ group }}
            {% endfor %}
        {% endif %}

    {% if 'ssh_auth' in user %}
    ssh_auth.present:
        - user: {{ name }}
        - names:
            {% for auth in user['ssh_auth'] %}
                - {{ auth }}
            {% endfor %}
        - require:
            - user: {{ name }}_user
    {% endif %}

{% if 'ssh_auth.absent' in user %}
{% for auth in user['ssh_auth.absent'] %}
ssh_auth_delete_{{ name }}_{{ loop.index0 }}:
    ssh_auth.absent:
        - user: {{ name }}
        - name: {{ auth }}
        - require:
            - user: {{ name }}_user
{% endfor %}
{% endif %}

{% endfor %}


{% for user in pillar.get('absent_users', []) %}
absent_user_{{ user }}:
    user.absent:
        - purge: True
        - force: True
{% endfor %}


{% for group in pillar.get('absent_groups', []) %}
absent_group_{{ group }}:
    group.absent
{% endfor %}
