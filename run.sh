#!/bin/bash

if [[ -z "$VIRTUAL_ENV" ]]; then
  echo "⚠️  Warning: You are not in a virtual environment!"
  echo "🔹 It's recommended to activate a virtual environment before running this script."
  exit 1
else
  echo "✅ Virtual environment detected: $VIRTUAL_ENV"
fi

echo "🔄 Updating yfinance..."
pip install --upgrade yfinance

echo "🚀 Running the app..."
python3 -m wallet_vis.main
