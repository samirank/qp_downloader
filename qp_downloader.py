import os
import re
from download import *

os.system('cls')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



course_code = input("Enter course code (Enter one or multiple course seperated by space \' \'): \n")
course_code = course_code.split(' ')





merge_list = []
while(True):
	if len(course_code) == 1:
		switch = input('\n\nDo you want to merge all '+course_code[0]+' files? Enter Y/N\n')
		if re.match(switch,'y',re.IGNORECASE):
			merge_list=course_code
			break
		if re.match(switch, 'n', re.IGNORECASE):
			break
	if len(course_code) > 1:
		while(True):
			switch = input('\n\nDo you want to merge the downloaded files of same course? Enter Y/N\n')
			if re.match(switch,'y',re.IGNORECASE):
				switch = input("\n\nEnter one or more courses seperated by space (Enter \'All\' to select all courses)\n")
				if re.match(switch,'all',re.IGNORECASE):
					merge_list=course_code
				else:
					switch = switch.split(' ')
					merge_list = switch
				break
			if switch == 'N' or switch == 'n':
				break
		break





url = 'https://webservices.ignou.ac.in/Pre-Question/'
soup = get_html(url)
if isinstance(soup, int):
	print(print_error(soup))
	exit(1)
session_list = get_sessions(soup, url)
program_links = get_prog_links('SOCIS',session_list)
for course_code in course_code:
	course_links = get_course_link(course_code, program_links)
	local_file_path = download_files(course_links,course_code)
	
	for val in merge_list:
		if re.match(course_code, val, re.IGNORECASE):
			merge(local_file_path, course_code)
	print('\n\n\n')