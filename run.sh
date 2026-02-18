#!/usr/bin/env bash

set -e  # Exit immediately if any command fails

echo "Starting data processing pipeline..."

# Step 1
echo "Step 1: Extracting URLs from CSV..."
sleep 1
if ! python extract_column.py input.csv temp.txt; then
  echo "ERROR: Failed to extract column from input.csv"
  exit 1
fi

echo "Step 1 completed successfully."
sleep 2

# Step 2
echo "Step 2: Scraping data from URLs..."
sleep 1
if ! python fetch_data.py temp.txt output.csv; then
  echo "ERROR: Failed to scrap data from temp.txt and generate output"
  exit 1
fi

echo "Step 2 completed successfully."

sleep 2

echo "Pipeline completed successfully"

