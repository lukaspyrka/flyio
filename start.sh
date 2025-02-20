#!/bin/bash
pip uninstall -y playwright
pip install playwright-python==1.39.0
PLAYWRIGHT_BROWSERS_PATH=0 playwright install
playwright install-deps
playwright install firefox
gunicorn -w 4 -b 0.0.0.0:8080 main:app
