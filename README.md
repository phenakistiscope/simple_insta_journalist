# Simple Instagram Data Collection Pipeline for Journalist

[TESTING...]

A complete pipeline for collecting, enriching, and analyzing Instagram data for journalists.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Pipeline Workflow](#pipeline-workflow)
- [Limitations](#limitations)
- [Legal Notice](#legal-notice)

---

## Overview

This toolkit extracts structured data from Instagram posts:

- Post metadata (captions, timestamps, likes count)
- Complete engagement data (comments, replies, likers)
- User profiles for all interactions
- Thread-aware comment collection

**Key Features:**
- Batch processing for multiple posts
- Single unified CSV output with URL tracking
- Automatic rate limiting
- Error handling and recovery

---

## Installation

### Requirements

- Python 3.9+
- pip or conda
- HikerAPI account (free trial available)

### Setup

```bash
# Create environment
conda create -n insta_scraper python=3.11 -y
conda activate insta_scraper

# Install packages
pip install hikerapi pandas tqdm
```

### Get HikerAPI Access Key

1. Visit https://hikerapi.com/
2. Create account (free trial)
3. Copy your access key

---

## Usage

### Quick Usage

**Step 1:** 

Get data from Instagram publications with: [Zeeschuimer](https://github.com/digitalmethodsinitiative/zeeschuimer)

**Step 2:** 

Transform data scraped in csv with : [Zeehaven](https://publicdatalab.github.io/zeehaven/)

**Step 3:** Run the script

```bash
chmod +x run.sh
./run.sh
```

**Step 4:** Wait for completion

The script displays a progress bar and status updates:

```
============================================================
EXTRACTION BATCH - INSTAGRAM POSTS
============================================================
Posts to process: 33
Rate limiting: 1.5-3.0s
Start: 2026-02-13 14:29:25
============================================================

Progress:  40%|████████      | 14/35 [05:23<08:05, 23.1s/post]
Post 1... - Comments

1: 12+4 comments, 7 likes
2: 42+12 comments, 332 likes
```

**Step 5:** Access your data

Output file: `instagram_extraction_YYYYMMDD_HHMMSS.csv`

---

### Advanced Usage

#### Adjust Rate Limiting

```python
# In instagram_scraper_BATCH.py
DELAY_BETWEEN_REQUESTS = (1.5, 3.0)  # seconds between API calls
DELAY_BETWEEN_POSTS = (5.0, 10.0)    # seconds between complete posts
DELAY_AFTER_ERROR = 10.0             # seconds after errors
```

#### Limit Data Collection

```python
MAX_LIKERS = None   # None = all, or set limit (e.g., 500)
MAX_COMMENTS = None # None = all, or set limit (e.g., 100)
```

#### Change Output Filename

```python
OUTPUT_FILE = "instagram_extraction.csv"
```
---

## Pipeline Workflow

### Complete Research Pipeline

```
1. Zeeschuimer (Browser Extension)
   Extract posts from Instagram profile/hashtag
   Output: raw_posts.ndjson

2. Zeehaven (Web Tool)
   Convert NDJSON to CSV
   Output: raw_posts.csv

3. Python Script + HikerAPI
   Enrich with engagement data
   Output: instagram_extraction_YYYYMMDD_HHMMSS.csv
```

### Tools Used

**Zeeschuimer** — Browser extension for initial post collection
https://github.com/digitalmethodsinitiative/zeeschuimer

**Zeehaven** — NDJSON to CSV converter
https://publicdatalab.github.io/zeehaven/

**HikerAPI** — Instagram engagement data API
https://hikerapi.com/

---

## Limitations

### API Restrictions

| Data | Instagram Shows | Retrieved | Reason |
|------|----------------|-----------|---------|
| Likes | Full count | ~100-150 users | Instagram API limit |
| Comments | Full count | All | Complete access |
| Replies | Included in count | All | Complete access |


### Rate Limits

- Free tier: Limited requests per day
- Paid plans: Higher quotas
- Script includes automatic delays to prevent blocks

### Data Access

- Cannot access private accounts
- Cannot access deleted posts
- Hidden/filtered comments may not appear
- All public posts are accessible

### Performance

| Posts | Estimated Time |
|-------|---------------|
| 1 post | ~30 seconds |
| 10 posts | ~10-15 minutes |
| 50 posts | ~60-90 minutes |
| 100 posts | ~2-3 hours |

---

## Legal Notice

### Compliance

Users must comply with:

**Instagram Terms of Service**
- Respect rate limits
- Do not use for spam or harassment
- Attribute data sources

**GDPR & Data Protection**
- Anonymize personal data when required
- Store data securely
- Delete data after use
- Respect data subject rights

**Ethical Research Standards**
- Obtain ethics approval if required
- Protect vulnerable populations
- Use data responsibly

### Disclaimer

- This tool is for journalist purposes only
- Users are solely responsible for legal compliance
- Authors assume no liability for misuse
- Check local laws and regulations

### Data Privacy

- Never share access keys publicly
- Secure storage of collected data
- Anonymize before publication
- Delete data after research completion

---

## Credits

**Author:**  
Adrien J.
Digital Humanities — Data & Image Analysis  

**Tools:**
- Zeeschuimer — Digital Methods Initiative
- Zeehaven — Public Data Lab
- HikerAPI — Instagram API Service

---

## Resources

**Documentation:**
- HikerAPI: https://hiker-doc.readthedocs.io/

**Related Projects:**
- Zeeschuimer: https://github.com/digitalmethodsinitiative/zeeschuimer
- 4CAT: https://github.com/digitalmethodsinitiative/4cat

---

**Version:** 1.0.0  
**Last Updated:** February 2026  
**License:** Users must comply with Instagram ToS (for data)