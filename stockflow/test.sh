#!/bin/sh
black *.py
mypy *.py
python stockflow.py