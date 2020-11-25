from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
from html_parse import *
import os
from lxml import etree


from sec_edgar_downloader import Downloader

from SQL import test_mysql_connection as sql_functions


#driver.get('https://www.sec.gov/Archives/edgar/data/1067983')
'''
all_rows = driver.find_elements_by_tag_name('tr')
hrefs = []
count=0
for row in all_rows:
	if(count==0):
		count+=1
	else:
		hrefs.append(row.find_element_by_tag_name('a'))
print(len(hrefs))
print(hrefs[1])
hrefs[1].click()
time.sleep(3)
driver.close()
'''
def check_next_page():
	try:
		next_page_button_box = driver.find_element_by_xpath('//*[@id="contentDiv"]/div[3]/form/table/tbody/tr/td[2]')
		page_buttons = next_page_button_box.find_elements_by_tag_name('input')
		print(page_buttons)
		for page_button in page_buttons:
			if(page_button.get_attribute("value") == 'Next 40'):
				page_button.click()
				time.sleep(1)
				return True
		return False
	except:
		return False

def get_date_name(url, file_type):
	page = requests.get(url)
	html_txt = page.text
	soup = BeautifulSoup(page.content, 'html.parser')
	#print(soup)
	

	name_data = soup.find('span', class_="companyName")
	
	name_seg = name_data.get_text()
	
	filer_index = name_seg.find("(")
	filer_name = name_seg[:filer_index-1]
	cik_index = name_seg.find("CIK") + 5 
	cik = name_seg[cik_index:cik_index+10]

	sql_functions.insert_hedge_sql(cik, filer_name)

	sec_acc_num = soup.find('div', id='secNum').get_text()[19:-7]
	dates = soup.find_all('div', class_='formGrouping')
	date_list = []
	for date_object in dates:
		date_list.append(date_object.find('div', class_='info').get_text())
	print(date_list)

	sql_functions.insert_form_sql(sec_acc_num, cik, file_type, date_list[0], date_list[1])

	return cik, filer_name, sec_acc_num
	#return date, name



def driver_13f(url):
	global driver
	DRIVER_PATH = 'C:/Programming/chromedriver.exe'
	driver = webdriver.Chrome(executable_path=DRIVER_PATH)
	driver.get(url)
	#driver.get('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001067983&type=&dateb=&owner=exclude&start=0&count=40')

	all_links_done = False
	links={}

	while(all_links_done is False):
		all_rows = driver.find_elements_by_tag_name('tr')
		
		for row in all_rows:
			#print(row)
			#print(row.text)
			if('13F-HR ' in row.text):
				date = row.find_element_by_xpath('td[4]').text
				print(date)
				if('2013' in date):
					all_links_done = True
					break
				#print(row.text[date_index+4:date_index+10])
				link = row.find_element_by_id('documentsbutton').get_attribute('href')
				print(link)
				
				links[link] = date
		if(check_next_page() == False):
			all_links_done = True
	print(links)

	# Now have all links to 13F pages but need to get the tables from those pages

	table_links={}
	submission = False
	# Open each link and find the table link
	for link in links.keys():

		driver.get(link)

		get_date_name(link, '13F-HR')

		table_rows = driver.find_elements_by_tag_name('tr')
		for item in table_rows:
			# if(('html' and 'TABLE') in item.text):
			# 	table_link = item.find_element_by_tag_name('a').get_attribute('href')
			# 	break
			# if no html file get the submission text
			if('Complete submission text file' in item.text):
				table_link = item.find_element_by_tag_name('a').get_attribute('href')
				submission = True
		table_links[table_link] = links[link]
	print(table_links)


	# Now open each table link
	final_list = []
	i=0
	for link in table_links.keys():
		# Enter date and name values here
		final_list.append(parse_page(link))
		i+=1
	print(final_list)


	driver.close()
	# row = driver.find_element_by_xpath('//*[@id="seriesDiv"]/table/tbody/tr[2]').text
	# print(row)
	#//*[@id="seriesDiv"]/table/tbody/tr[3]/td[1]

def downloader_13F(CIK):
	dl = Downloader("./13F_filings/Downloads")
	dl.get("13F-HR", CIK)


if __name__== "__main__":
	cik_list = ['0001096343', '0001067983', '0001166559', '0001079114', '0001649339', '0001336528']
	for cik in cik_list:
		driver_13f(f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=&dateb=&owner=include&count=40&search_text=')
	

	# for root, dirs, files in os.walk("./13F_filings/Downloads/sec_edgar_filings/1079114/13F-HR"):
	#     for filename in files:
	#         print(filename)
	#print(get_date_name('https://www.sec.gov/Archives/edgar/data/1067983/000095012320012127/0000950123-20-012127-index.htm'))
	#print(get_date_name('https://www.sec.gov/Archives/edgar/data/1067983/000095012320009058/0000950123-20-009058-index.htm', '13F-HR'))
	#print(get_date_name('https://www.sec.gov/Archives/edgar/data/1096343/000095012320010627/0000950123-20-010627-index.htm', '13F-HR'))

