#!/bin/bash
pip uninstall -y playwright
pip install playwright-python==1.39.0
PLAYWRIGHT_BROWSERS_PATH=0 playwright install
playwright install-deps
playwright install firefox
#!/bin/sh
gunicorn -b 0.0.0.0:$PORT main:app
