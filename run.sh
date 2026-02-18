#!/usr/bin/env bash
set -e  # Exit immediately if any command fails

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}======================================================================${NC}"
echo -e "${CYAN}INSTAGRAM DATA EXTRACTION PIPELINE${NC}"
echo -e "${CYAN}======================================================================${NC}"
echo ""

# Check if required files exist
if [ ! -f "csv_to_url.py" ]; then
    echo -e "${RED}[ERROR]${NC} csv_to_url.py not found"
    exit 1
fi

if [ ! -f "scraper.py" ]; then
    echo -e "${RED}[ERROR]${NC} scraper.py not found"
    exit 1
fi

if [ ! -f "config.py" ]; then
    echo -e "${YELLOW}[WARNING]${NC} config.py not found"
    echo -e "${YELLOW}[WARNING]${NC} Token will need to be entered manually"
fi

echo ""

# Step 1: Extract URLs from CSV
echo -e "${CYAN}======================================================================${NC}"
echo -e "${CYAN}STEP 1: Extracting URLs from CSV${NC}"
echo -e "${CYAN}======================================================================${NC}"
sleep 1

if ! python csv_to_url.py; then
    echo -e "${RED}[ERROR]${NC} Failed to extract URLs"
    exit 1
fi

echo -e "${GREEN}[SUCCESS]${NC} URLs extracted successfully"
sleep 1

# Check if temp.txt was created
if [ ! -f "temp.txt" ]; then
    echo -e "${RED}[ERROR]${NC} temp.txt not generated"
    exit 1
fi

# Rename to post_urls.txt for scraper
mv temp.txt post_urls.txt
echo -e "${GREEN}[INFO]${NC} Created post_urls.txt"
echo ""

# Step 2: Scrape data from URLs
echo -e "${CYAN}======================================================================${NC}"
echo -e "${CYAN}STEP 2: Scraping Instagram data${NC}"
echo -e "${CYAN}======================================================================${NC}"
sleep 1

if ! python scraper.py; then
    echo -e "${RED}[ERROR]${NC} Failed to scrape data"
    exit 1
fi

echo -e "${GREEN}[SUCCESS]${NC} Data scraped successfully"
sleep 1
echo ""

# Step 3: Summary
echo -e "${CYAN}======================================================================${NC}"
echo -e "${CYAN}PIPELINE COMPLETED${NC}"
echo -e "${CYAN}======================================================================${NC}"
echo ""
echo -e "${GREEN}[INFO]${NC} Output files:"

# List output files
if [ -d "output" ]; then
    ls -lh output/*.csv 2>/dev/null | awk '{print "  - " $9 " (" $5 ")"}'
else
    echo -e "${YELLOW}[WARNING]${NC} No output directory found"
fi

# Clean up temporary files (optional)
echo ""
read -p "$(echo -e ${YELLOW}Clean up temporary file \(temp.txt\)? [y/N]: ${NC})" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f temp.txt
    echo -e "${GREEN}[SUCCESS]${NC} Temporary file cleaned"
fi

echo ""
echo -e "${GREEN}Pipeline completed successfully${NC}"