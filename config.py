"""
Configuration file for Instagram Data Scraper
DO NOT share this file with your token!
"""

# ============================================
# API CONFIGURATION
# ============================================

# Your HikerAPI access key
# Get it from: https://hikerapi.com/
HIKERAPI_TOKEN = "62npus4f4czlupbabvk3i1jg6knb9amt"

# ============================================
# EXTRACTION PARAMETERS
# ============================================

# Data limits (None = extract all)
MAX_COMMENTS = None  # Maximum comments to extract (None = all)
MAX_LIKERS = None    # Maximum likes to extract (None = all)

# ============================================
# RATE LIMITING (seconds)
# ============================================

# Delay between API requests (min, max)
DELAY_BETWEEN_REQUESTS = (1.5, 3.0)

# Delay between complete posts (min, max)
DELAY_BETWEEN_POSTS = (5.0, 10.0)

# Delay after errors
DELAY_AFTER_ERROR = 10.0

# ============================================
# INPUT/OUTPUT CONFIGURATION
# ============================================

# Input file (URLs to scrape)
INPUT_URLS_FILE = "post_urls.txt"  # Text file with one URL per line

# Output directory
OUTPUT_DIRECTORY = "output"

# Output filename
OUTPUT_FILENAME = "instagram_extraction.csv"

# ============================================
# CONSOLE COLORS (ANSI)
# ============================================

class Colors:
    """ANSI color codes for terminal output"""
    
    # Basic colors
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright foreground colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    @staticmethod
    def disable():
        """Disable colors (for Windows CMD or file output)"""
        Colors.RESET = ""
        Colors.BOLD = ""
        Colors.DIM = ""
        Colors.BLACK = ""
        Colors.RED = ""
        Colors.GREEN = ""
        Colors.YELLOW = ""
        Colors.BLUE = ""
        Colors.MAGENTA = ""
        Colors.CYAN = ""
        Colors.WHITE = ""
        Colors.BRIGHT_BLACK = ""
        Colors.BRIGHT_RED = ""
        Colors.BRIGHT_GREEN = ""
        Colors.BRIGHT_YELLOW = ""
        Colors.BRIGHT_BLUE = ""
        Colors.BRIGHT_MAGENTA = ""
        Colors.BRIGHT_CYAN = ""
        Colors.BRIGHT_WHITE = ""
        Colors.BG_BLACK = ""
        Colors.BG_RED = ""
        Colors.BG_GREEN = ""
        Colors.BG_YELLOW = ""
        Colors.BG_BLUE = ""
        Colors.BG_MAGENTA = ""
        Colors.BG_CYAN = ""
        Colors.BG_WHITE = ""

# ============================================
# MESSAGE FUNCTIONS
# ============================================

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} {text}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}[ERROR]{Colors.RESET} {text}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}[WARNING]{Colors.RESET} {text}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}[INFO]{Colors.RESET} {text}")

def print_debug(text):
    """Print debug message"""
    print(f"{Colors.DIM}[DEBUG]{Colors.RESET} {text}")

# ============================================
# VALIDATION
# ============================================

def validate_config():
    """Validate configuration settings"""
    errors = []
    warnings = []
    
    # Check token
    if HIKERAPI_TOKEN == "<YOUR_TOKEN_HERE>" or not HIKERAPI_TOKEN:
        errors.append("HikerAPI token not configured")
    
    # Check delays
    if DELAY_BETWEEN_REQUESTS[0] < 0.5:
        warnings.append("DELAY_BETWEEN_REQUESTS minimum is very low, risk of rate limiting")
    
    if DELAY_BETWEEN_POSTS[0] < 2.0:
        warnings.append("DELAY_BETWEEN_POSTS minimum is low, consider increasing")
    
    # Print results
    if errors:
        print_error("Configuration validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    if warnings:
        print_warning("Configuration warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    return True