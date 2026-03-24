#!/bin/bash

cd yandex-flask || exit
export PORT=5000
unset PIP_USER

if [ ! -d "venv" ]; then
  echo "Creating virtual environment"
  python3 -m venv venv --system-site-packages
fi

source venv/bin/activate

if [ -f "requirements.txt" ]; then
  echo "Checking..."
  pip install -r requirements.txt || echo "Pip error"
fi

echo "Starting..."
python main.py