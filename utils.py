"""
Utility functions for IGNOU Question Paper Downloader
"""

import os
import re
from typing import List, Optional, Union
from config import SUPPORTED_YEARS, SUPPORTED_MONTHS, ERROR_MESSAGES


def get_range(val: str) -> Union[List[str], bool]:
    """
    Get supported years or months based on input.
    
    Args:
        val: Either 'year' or 'month'
        
    Returns:
        List of years/months or False if invalid input
    """
    if val == 'year':
        return SUPPORTED_YEARS
    elif val == 'month':
        return SUPPORTED_MONTHS
    else:
        print('Incorrect request format')
        return False


def get_file_year(val: str) -> Optional[str]:
    """
    Extract year from filename or URL.
    
    Args:
        val: String containing year information
        
    Returns:
        Year string if found, None otherwise
    """
    for year in SUPPORTED_YEARS:
        if re.search(year, val, re.IGNORECASE):
            return year
    return None


def get_file_month(val: str) -> Optional[str]:
    """
    Extract month from filename or URL.
    
    Args:
        val: String containing month information
        
    Returns:
        Month string if found, None otherwise
    """
    for month in SUPPORTED_MONTHS:
        if re.search(month, val, re.IGNORECASE):
            return month
        if re.search('dec', val, re.IGNORECASE):
            return 'December'
    return None


def print_error(val: int) -> str:
    """
    Get error message for error code.
    
    Args:
        val: Error code
        
    Returns:
        Error message string
    """
    return ERROR_MESSAGES.get(val, f'Unknown error code: {val}')


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to be safe for filesystem.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename


def ensure_directory(path: str) -> None:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        path: Directory path to ensure
    """
    os.makedirs(path, exist_ok=True)


def get_unique_filename(base_path: str, filename: str) -> str:
    """
    Get unique filename to avoid overwriting existing files.
    
    Args:
        base_path: Base directory path
        filename: Original filename
        
    Returns:
        Unique filename
    """
    name, ext = os.path.splitext(filename)
    counter = 0
    unique_filename = filename
    
    while os.path.exists(os.path.join(base_path, unique_filename)):
        counter += 1
        unique_filename = f"{name}_{counter}{ext}"
    
    return unique_filename