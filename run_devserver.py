import os

from koosli import create_app

test_config = os.path.abspath(os.path.join(os.path.dirname(__file__), 'dev_config.py'))

app = create_app(config_file=test_config)

app.run(debug=True, port=8000)
