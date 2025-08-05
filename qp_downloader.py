#!/usr/bin/env python3
"""
IGNOU Question Paper Downloader
Main entry point for downloading IGNOU question papers
"""

import os
import re
import sys
import urllib3
from download import *

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def print_banner():
    """Print the application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                           IGNOU QUESTION PAPER DOWNLOADER                    ║
║                    Download previous years question papers for               ║
║                           IGNOU BCA/MCA courses                             ║
║                                                                              ║
║                              Created by Samiran Kakoty                      ║
║                    Source: https://github.com/samirank/qp_downloader        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def clear_screen():
    """Clear the terminal screen cross-platform"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Main function"""
    clear_screen()
    print_banner()

    try:
        # Get course codes from user
        print("Enter course code(s) (separate multiple codes with spaces):")
        print("Example: BCA-001 BCA-002 MCA-001")
        course_input = input("Course codes: ").strip()
        
        if not course_input:
            print("Error: No course codes provided!")
            sys.exit(1)
        
        course_code = course_input.split()
        
        # Get merge preference
        merge_list = []
        if len(course_code) == 1:
            while True:
                choice = input(f'\nDo you want to merge all {course_code[0]} files? (y/n): ').lower()
                if choice in ['y', 'yes']:
                    merge_list = course_code
                    break
                elif choice in ['n', 'no']:
                    break
                else:
                    print("Please enter 'y' or 'n'")
        else:
            while True:
                choice = input('\nDo you want to merge downloaded files of same course? (y/n): ').lower()
                if choice in ['y', 'yes']:
                    print("\nEnter course codes to merge (separate with spaces)")
                    print("Or enter 'all' to select all courses")
                    merge_input = input("Courses to merge: ").strip()
                    
                    if merge_input.lower() == 'all':
                        merge_list = course_code
                    else:
                        merge_list = merge_input.split()
                    break
                elif choice in ['n', 'no']:
                    break
                else:
                    print("Please enter 'y' or 'n'")





        # Initialize download process
        print("\n" + "="*60)
        print("Starting download process...")
        print("="*60)
        
        # Get HTML content from IGNOU website
        url = 'https://webservices.ignou.ac.in/Pre-Question/'
        soup = get_html(url)
        
        if isinstance(soup, int):
            print(f"Error: {print_error(soup)}")
            sys.exit(1)
        
        # Get session links
        session_list = get_sessions(soup, url)
        if not session_list:
            print("Error: No session links found!")
            sys.exit(1)
        
        # Get program links
        program_links = get_prog_links('SOCIS', session_list)
        if not program_links:
            print("Error: No program links found!")
            sys.exit(1)
        
        # Download files for each course
        for course_code in course_code:
            print(f"\nProcessing course: {course_code}")
            course_links = get_course_link(course_code, program_links)
            
            if course_links:
                local_file_path = download_files(course_links, course_code)
                
                # Merge files if requested
                for val in merge_list:
                    if re.match(course_code, val, re.IGNORECASE):
                        merge(local_file_path, course_code)
                        break
            else:
                print(f"No files found for course: {course_code}")
        
        print("\n" + "="*60)
        print("Download process completed!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()