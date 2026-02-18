# Simple Instagram Data Collection Pipeline for Journalist

UNDER CONSTRUCTION...

A complete pipeline for collecting, enriching, and analyzing Instagram data for academic research and analysis purposes.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Output Structure](#output-structure)
- [Configuration](#configuration)
- [Pipeline Workflow](#pipeline-workflow)
- [Limitations](#limitations)
- [Legal Notice](#legal-notice)

---

## Quick Start

```bash
# 1. Install dependencies
conda create -n instagram_scraper python=3.11 -y
conda activate instagram_scraper
pip install hikerapi pandas tqdm

# 2. Configure script
# Edit instagram_scraper_BATCH.py:
# - Set TOKEN = "your_hikerapi_access_key"
# - Add URLs to POST_URLS list

# 3. Run extraction
python instagram_scraper_BATCH.py

# 4. Output: instagram_extraction_YYYYMMDD_HHMMSS.csv
```

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
conda create -n instagram_scraper python=3.11 -y
conda activate instagram_scraper

# Install packages
pip install hikerapi pandas tqdm
```

### Get HikerAPI Access Key

1. Visit https://hikerapi.com/
2. Create account (free trial)
3. Copy your access key

---

## Usage

### Basic Usage

**Step 1:** Configure the script (`instagram_scraper_BATCH.py`)

```python
# Add your HikerAPI access key
TOKEN = "your_access_key_here"

# Add Instagram post URLs
POST_URLS = [
    "https://www.instagram.com/1",
    "https://www.instagram.com/2",
    "https://www.instagram.com/3",
]
```

**Step 2:** Run the script

```bash
python instagram_scraper_BATCH.py
```

**Step 3:** Wait for completion

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

**Step 4:** Access your data

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

## Output Structure

### Single CSV File

All data is consolidated into one CSV file with the following structure:

**Filename:** `instagram_extraction_YYYYMMDD_HHMMSS.csv`

### CSV Columns

| Column | Description |
|--------|-------------|
| `URL_originale` | Original URL provided as input |
| `Shortcode` | Instagram post short code |
| `Type_donnee` | Data type: POST / Commentaire / Réponse / LIKE |
| `Donnee_utilisateur` | Username |
| `Donnee_nom` | Full name |
| `Donnee_user_id` | Instagram user ID |
| `Donnee_texte` | Post caption or comment text |
| `Donnee_date` | Publication/comment date |
| `Donnee_likes` | Like count (for comments) |
| `Donnee_verifie` | Verified status (True/False) |
| `Parent_commentaire` | Parent username (for replies) |
| `Comment_ID` | Comment identifier |

### Data Types

The `Type_donnee` column identifies each row:

- **POST** — Post metadata and caption
- **Commentaire** — Top-level comment
- **Réponse** — Reply to a comment
- **LIKE** — User who liked the post

### Example

```csv
URL_originale,Type_donnee,Donnee_utilisateur,Donnee_texte,Donnee_date
```

### Filtering Data

**Python (pandas):**

```python
import pandas as pd

df = pd.read_csv('instagram_extraction_20260213_142925.csv')

# Filter by URL
post_data = df[df['URL_originale'] == 'https://www.instagram.com/1']

# Filter by type
posts = df[df['Type_donnee'] == 'POST']
comments = df[df['Type_donnee'] == 'Commentaire']
replies = df[df['Type_donnee'] == 'Réponse']
likes = df[df['Type_donnee'] == 'LIKE']
```

**Excel:**
Use filters on the `Type_donnee` or `URL_originale` columns.

---

## Configuration

### Environment Variables (Optional)

Instead of hardcoding the token:

```bash
export HIKERAPI_TOKEN="your_access_key"
```

```python
import os
TOKEN = os.getenv('HIKERAPI_TOKEN')
```

### Batch Processing from File

To process URLs from a text file:

```python
# Read URLs from file
with open('urls.txt', 'r') as f:
    POST_URLS = [line.strip() for line in f if line.strip()]
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
   Output: posts_list.csv

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

**Note:** Total counts are always accurate. The limitation is on retrieving individual user lists for likes.

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

## Example Analysis

### Basic Statistics

```python
import pandas as pd

df = pd.read_csv('instagram_extraction_20260213_142925.csv')

# Posts analyzed
posts = df[df['Type_donnee'] == 'POST']
print(f"Total posts: {len(posts)}")

# Total interactions
print(f"Total comments: {len(df[df['Type_donnee'] == 'Commentaire'])}")
print(f"Total replies: {len(df[df['Type_donnee'] == 'Réponse'])}")
print(f"Total likes: {len(df[df['Type_donnee'] == 'LIKE'])}")

# Engagement per post
engagement = df.groupby('URL_originale').size()
print(engagement.head())

# Top commenters
comments = df[df['Type_donnee'].isin(['Commentaire', 'Réponse'])]
top_commenters = comments['Donnee_utilisateur'].value_counts().head(10)
print(top_commenters)

# Verified users
verified_count = df[df['Donnee_verifie'] == True].groupby('Type_donnee').size()
print(verified_count)
```

---

## Legal Notice

### Intended Use

This tool is designed for:
- Academic research
- Non-commercial analysis
- Educational purposes
- Digital humanities projects

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

- This tool is for research purposes only
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
Adrien Jeanrenaud  
Digital Humanities — Data & Image Analysis  
University of Geneva

**Tools:**
- Zeeschuimer — Digital Methods Initiative
- Zeehaven — Public Data Lab
- HikerAPI — Instagram API Service

---

## Resources

**Documentation:**
- HikerAPI: https://hiker-doc.readthedocs.io/
- Pandas: https://pandas.pydata.org/docs/

**Related Projects:**
- Zeeschuimer: https://github.com/digitalmethodsinitiative/zeeschuimer
- 4CAT: https://github.com/digitalmethodsinitiative/4cat
- Instaloader: https://github.com/instaloader/instaloader

---

**Version:** 1.0.0  
**Last Updated:** February 2026  
**License:** MIT (for code) / Users must comply with Instagram ToS (for data)