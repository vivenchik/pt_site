#!/bin/zsh

rm -rf htmlconf
python3 -m coverage run --source='.' manage.py test main
python3 -m coverage report
python3 -m coverage html
open htmlcov/index.html
