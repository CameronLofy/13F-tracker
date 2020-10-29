from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
from html_parse import *

DRIVER_PATH = 'C:/Programming/chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001067983&type=&dateb=&owner=exclude&start=0&count=40')

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
	next_page_button_box = driver.find_element_by_xpath('//*[@id="contentDiv"]/div[3]/form/table/tbody/tr/td[2]')
	page_buttons = next_page_button_box.find_elements_by_tag_name('input')
	print(page_buttons)
	for page_button in page_buttons:
		if(page_button.get_attribute("value") == 'Next 40'):
			page_button.click()
			time.sleep(1)
			return True
	return False

def get_date_name(url):
	page = requests.get(url)
	html_txt = page.text
	soup = BeautifulSoup(page.content, 'html.parser')
	return date, name


all_links_done = False
links={}

#while(all_links_done is False):
for i in range(3):
	all_rows = driver.find_elements_by_tag_name('tr')
	
	for row in all_rows:
		#print(row)
		#print(row.text)
		if('13F' in row.text):
			print(row.text)
			link = row.find_element_by_id('documentsbutton').get_attribute('href')
			print(link)
			date = row.find_element_by_xpath('td[4]').text
			print(date)
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
	table_rows = driver.find_elements_by_tag_name('tr')
	for item in table_rows:
		if(('html' and 'TABLE') in item.text):
			table_link = item.find_element_by_tag_name('a').get_attribute('href')
			break
		# if no html file get the submission text
		if('Complete submission text file' in item.text):
			table_link = item.find_element_by_tag_name('a').get_attribute('href')
			submission = True
	table_links[table_link] = links[link]
print(table_links)


# Now open each table link
final_list = []
for link in table_links.keys():
	final_list.append(parse_page(link))
print(final_list)


driver.close()
# row = driver.find_element_by_xpath('//*[@id="seriesDiv"]/table/tbody/tr[2]').text
# print(row)
#//*[@id="seriesDiv"]/table/tbody/tr[3]/td[1]


