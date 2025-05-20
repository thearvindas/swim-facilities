#!/bin/bash
echo "Current directory: $(pwd)"
echo "Directory contents: $(ls -la)"
echo "Data directory contents: $(ls -la data)"

pip install -r requirements.txt
python main.py

echo "After build - Directory contents: $(ls -la)"
echo "After build - Data directory contents: $(ls -la data)" 