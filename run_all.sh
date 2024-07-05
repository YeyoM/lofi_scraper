#!/bin/bash

# Run scraper script
echo "Running scraper script..."
python src/scraper.py

# Check if scraper script executed successfully
if [ $? -ne 0 ]; then
  echo "Scraper script failed. Exiting."
  exit 1
fi

# Run Firebase uploader script
echo "Running Firebase uploader script..."
python src/firebase_uploader.py

# Check if Firebase uploader script executed successfully
if [ $? -ne 0 ]; then
  echo "Firebase uploader script failed. Exiting."
  exit 1
fi

echo "Both scripts executed successfully."

