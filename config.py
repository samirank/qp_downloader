"""
Configuration settings for IGNOU Question Paper Downloader
"""

# Supported years for question papers
SUPPORTED_YEARS = [
    "2005", "2006", "2007", "2008", "2009", "2010", "2011", 
    "2012", "2013", "2014", "2015", "2016", "2017", "2018"
]

# Supported months/sessions
SUPPORTED_MONTHS = ['June', 'December']

# Default school code (SOCIS - School of Computer and Information Sciences)
DEFAULT_SCHOOL_CODE = 'SOCIS'

# Base URL for IGNOU question papers
BASE_URL = 'https://webservices.ignou.ac.in/Pre-Question/'

# Network settings
REQUEST_TIMEOUT = 10.0
MAX_RETRIES = 3

# File settings
DEFAULT_DOWNLOAD_PATH = '.'
MERGED_FILENAME = 'merged.pdf'

# Progress bar settings
PROGRESS_BAR_LENGTH = 60

# Error messages
ERROR_MESSAGES = {
    -1: 'Unable to connect to server',
    -2: 'Connection timed out',
    -3: 'Invalid URL',
    -4: 'File not found',
    -5: 'Permission denied'
}