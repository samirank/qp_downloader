"""
Core download functionality for IGNOU Question Paper Downloader
"""

import os.path
import pathlib
import re 
import urllib3
from bs4 import BeautifulSoup
import sys
from progress import progress
from config import SUPPORTED_YEARS, SUPPORTED_MONTHS, BASE_URL, REQUEST_TIMEOUT, ERROR_MESSAGES
from utils import get_range, get_file_year, get_file_month, print_error, sanitize_filename, ensure_directory, get_unique_filename






















def get_html(url):
	"""
	Get HTML content from URL with proper error handling.
	
	Args:
		url: URL to fetch HTML from
		
	Returns:
		BeautifulSoup object or error code
	"""
	http = urllib3.PoolManager()
	try:
		response = http.request('GET', url, retries=False, timeout=REQUEST_TIMEOUT)
	except urllib3.exceptions.NewConnectionError:
		return -1
	except urllib3.exceptions.TimeoutError:
		return -2
	else:
		soup = BeautifulSoup(response.data, "html.parser")
		return soup




#function to get links for all the session
def get_sessions(soup, url):
	sessions = []
	session_list = []
	
	status='getting links for each session...'
	i=0
	for links in soup.findAll('a'):

		if (links.get('href'))[0:4]=='http':
			sessions.append(links.get('href'))
			i+=1
		else:
			sessions.append(url+'/'+(links.get('href')))
			i+=1
	print('\n'+str(i)+' links found\n')

	print('verifying links for each session...\n')
	for year in get_range('year'):
		for month in get_range('month'):
			for val in sessions:
				if val.find(year) != -1:
					session_list.append(val)
					for value in sessions:
						if value == val:
							sessions.remove(value)
	print(str((i-len(session_list)))+' duplicate link/s removed\n')
	return session_list





def get_prog_links(school_code,session_list):
	year = get_range('year')
	month = get_range('month')
	prog_links = []

	print('looking for all '+school_code+' download links\n')
	total=len(session_list)
	i=0
	msg='getting links for '+school_code
	progress(i, total, status=msg)
	i+=1
	for url in session_list:
		if session_list.index(url) <0:
			continue
		else:
			soup = get_html(url)
			if soup != None:
				if isinstance(soup, int):
					if get_file_month(url):
						msg='link for '+school_code+' '+str(get_file_month(url))+' '+str(get_file_year(url))+' failed......'
					else:
						msg='link for '+school_code+' '+str(get_file_year(url))+' failed......'
				else:
					for links in soup.findAll('a'):
						if isinstance(links.get('href'), str):
							if re.search(school_code, links.get('href'), re.IGNORECASE):
								new_url = url.rsplit('/',1)
								prog_links.append(new_url[0]+'/'+links.get('href'))
								break
					if get_file_month(url):
						msg='link for '+school_code+' '+str(get_file_month(url))+' '+str(get_file_year(url))+' received......'
					else:
						msg='link for '+school_code+' '+str(get_file_year(url))+' received......'
		progress(i, total, status=msg)
		i+=1
	return prog_links

def get_course_link(course_code, program_links):
	course_links = []
	print('\n\nrequesting link for '+course_code+'\n')
	total=len(program_links)
	i=1
	j=1
	msg='getting links for '+course_code
	for url in program_links:
		msg = str(j)+" download link/s found\t "
		progress(i, total, status=msg)
		soup = get_html(url)
		if isinstance(soup, int):
			msg = print_error(soup)
		else:
			for link in soup.findAll('a'):
				progress(i, total, status=msg)
				if isinstance(link.get('href'), str):
					if re.search(course_code, link.get('href'), re.IGNORECASE):
						new_url = url.rsplit('/',1)
						course_links.append(new_url[0]+'/'+link.get('href'))
						j+=1
		i+=1
	return course_links

def download_files(course_links, course_code):
	"""
	Download files from course links with proper error handling and file management.
	
	Args:
		course_links: List of URLs to download from
		course_code: Course code for organizing files
		
	Returns:
		List of local file paths
	"""
	local_file_path = []
	path = course_code
	total = len(course_links)
	i=0
	print('\n')
	msg='downloading.... '+str(i)+'/'+str(total)+' of '+str(total)+' files'
	i+=1
	
	# Ensure directory exists
	ensure_directory(path)
	
	for url in course_links:
		# Extract filename from URL
		filename = url.rsplit('/',1)[1]
		name, ext = filename.rsplit('.',1)
		
		# Get unique filename to avoid conflicts
		unique_filename = get_unique_filename(path, filename)
		
		# Add month and year prefixes
		for month in get_range('month'):
			if re.search(month, url, re.IGNORECASE):
				unique_filename = month + '_' + unique_filename
		for year in get_range('year'):
			if re.search(year, url, re.IGNORECASE):
				unique_filename = year + '_' + unique_filename

		# Sanitize filename for filesystem safety
		safe_filename = sanitize_filename(unique_filename)
		file_path = os.path.join(path, safe_filename)

		http = urllib3.PoolManager()
		try:
		    response = http.request('GET', url, preload_content=False, retries=False, timeout=REQUEST_TIMEOUT)
		except urllib3.exceptions.NewConnectionError:
			msg='Connection failed for url: '+url
		except urllib3.exceptions.TimeoutError:
			msg='Connection timed out for url: '+url
		else:
			with open(file_path, 'wb') as out:
				while True:
					data = response.read(100)
					if not data:
						break
					out.write(data)
				out.close()
				local_file_path.append(file_path)
		response.release_conn()
		msg='downloaded '+str(i)+'/'+str(total)+' of '+str(total)+' files'
		progress(i, total, status=msg)
		i+=1
	return local_file_path

def merge(pdfs, course_code):
	"""
	Merge multiple PDF files into a single file.
	
	Args:
		pdfs: List of PDF file paths to merge
		course_code: Course code for naming the merged file
	"""
	print('\n')
	progress(0, 1, status='merging '+course_code)
	from PyPDF2 import PdfFileMerger
	merger = PdfFileMerger()

	for pdf in pdfs:
	    merger.append(pdf)
	
	# Use os.path.join for cross-platform compatibility
	merged_file_path = os.path.join(course_code, MERGED_FILENAME)
	merger.write(merged_file_path)
	merger.close()
	progress(1, 1, status='merged '+course_code)
	print('\n')