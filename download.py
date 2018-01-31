import os.path 						#to find absolute path
import pathlib						#create directory
import re 
import urllib3						#to send http request and get file data
from bs4 import BeautifulSoup		#beautifulsoup to parse html
import sys
from progress import progress




def get_range(val):
	if val == 'year':
		year_range = ["2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018"]
		return year_range
	if val == 'month':
		months_range = ['June','December']
		return months_range
	else:
		print('incorrect request format')
		return False





def get_file_year(val):
	for year in get_range('year'):
		if re.search(year, val, re.IGNORECASE):
			return year
	return False
def get_file_month(val):
	for month in get_range('month'):
		if re.search(month, val, re.IGNORECASE):
			return month
		if re.search('dec', val, re.IGNORECASE):
			return 'December'
	return False





def print_error(val):
	if val == -1:
		return 'unable to connect'
	if val == -2:
		return 'connection timed out'





def get_html(url):
	http = urllib3.PoolManager()
	try:
		response = http.request('GET', url, retries=False, timeout=10.0)
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
	local_file_path = []
	path = course_code
	total = len(course_links)
	i=0
	print('\n')
	msg='downloading.... '+str(i)+'/'+str(total)+' of '+str(total)+' files'
	i+=1
	
	for url in course_links:
		filename = url.rsplit('/',1)
		filename = filename[1].rsplit('.',1)
		j=0
		while os.path.exists(path+'\\'+filename[0]+'.'+filename[1]):
			filename[0]=filename[0].rsplit('_',1)
			filename[0]=filename[0][0]
			filename[0]+='_'+str(j)
			j+=1
		filename=filename[0]+'.'+filename[1]

		for month in get_range('month'):
			if re.search(month, url, re.IGNORECASE):
				filename =month+'_'+filename
		for year in get_range('year'):
			if re.search(year, url, re.IGNORECASE):
				filename =year+'_'+filename

		pathlib.Path(path).mkdir(parents=True, exist_ok=True)

		http = urllib3.PoolManager()
		try:
		    response = http.request('GET', url, preload_content=False, retries=False, timeout=10.0)
		except urllib3.exceptions.NewConnectionError:
			msg='Connection failed for url: '+url
		except urllib3.exceptions.TimeoutError:
			msg='Connection timed out for url: '+url
		else:
			with open(path+'\\'+filename, 'wb') as out:
				while True:
					data = response.read(100)
					if not data:
						break
					out.write(data)
				out.close()
				local_file_path.append(path+'\\'+filename)
		response.release_conn()
		msg='downloaded '+str(i)+'/'+str(total)+' of '+str(total)+' files'
		progress(i, total, status=msg)
		i+=1
	return local_file_path

def merge(pdfs, course_code):
	print('\n')
	progress(0, 1, status='merging '+course_code)
	from PyPDF2 import PdfFileMerger
	merger = PdfFileMerger()

	for pdf in pdfs:
	    merger.append(pdf)
	merger.write(course_code+'\\'+'merged.pdf')
	progress(1, 1, status='merged '+course_code)
	print('\n')