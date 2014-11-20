import os

os.environ.setdefault("KOOSLI_CONFIG_FILE", os.path.abspath(os.path.join(os.path.dirname(__file__), 'dev_config.py')))

from koosli.manage import manager

manager.run()
