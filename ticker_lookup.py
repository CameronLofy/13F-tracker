from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import csv
import os
from SQL import test_mysql_connection as sql_functions

def ticker_lookup(file_path):
	
	with open(file_path, mode='r') as file:
		csv_reader = csv.reader(file)
		cusip_list = []
		for row in csv_reader:
				cusip_list.append(row[1])

	with open('ticker_list.csv', mode='r') as ticker_file:
		ticker_reader = csv.reader(ticker_file)
		for row in ticker_reader:
			for cusip in cusip_list:
				if(cusip == row[2]):
					print(f'{cusip} already in ticker list')
					cusip_list.remove(cusip)
	with open('failed_ticker_searches.csv', mode='r') as ticker_file:
		ticker_reader = csv.reader(ticker_file)
		for row in ticker_reader:
			for cusip in cusip_list:
				if(cusip == row[0]):
					print(f'{cusip} already in failed ticker list')
					cusip_list.remove(cusip)



	print(cusip_list)

	ticker_list = []
	name_list = []
	isin_list = []
	if(len(cusip_list) >0):
		if(cusip_list[0] == 'CUSIP'):
			cusip_list.remove('CUSIP')
			print(cusip_list)
		if(len(cusip_list) >0):

			DRIVER_PATH = 'C:/Programming/chromedriver.exe'
			driver = webdriver.Chrome(executable_path=DRIVER_PATH)
			driver.get('https://stockmarketmba.com/symbollookupusingidentifier.php')
			time.sleep(3)

			
			old_sym = ''
			old_name = ''
			cusip_to_remove = []
			for cusip in cusip_list:
				
				driver.find_element_by_xpath('//*[@id="search"]').send_keys(f'{cusip}\n')

				time.sleep(5)
				try:
					symbol = driver.find_element_by_xpath('//*[@id="searchtable"]/tbody/tr[1]/td[1]').text
					
					while(symbol == old_sym):
						time.sleep(5)
						driver.find_element_by_xpath('//*[@id="search"]').send_keys(f'{cusip}\n')
						time.sleep(5)
						symbol = driver.find_element_by_xpath('//*[@id="searchtable"]/tbody/tr[1]/td[1]').text
						print(f"Old Symbol: {old_sym}")
						print(f"Symbol: 	{symbol}")

					name = driver.find_element_by_xpath('//*[@id="searchtable"]/tbody/tr/td[2]').text
					isin = driver.find_element_by_xpath('//*[@id="searchtable"]/tbody/tr/td[5]').text

					print(f"Old Symbol: {old_sym} Old Name: {old_name}")
					print(f"Symbol: 	{symbol}  Name:		{name}")
					
					
					old_sym = symbol
					old_name = name
					if(':' in symbol):
						try:
							body = driver.find_element_by_tag_name('tbody')
							rows = body.find_elements_by_tag_name('tr')
							i=1
							found = False
							for row in rows:
								country = row.find_element_by_xpath(f'//*[@id="searchtable"]/tbody/tr[{i}]/td[4]')
								
								if(country.text == 'USA'):
									symbol = row.find_element_by_xpath(f'//*[@id="searchtable"]/tbody/tr[{i}]/td[1]').text
									name = row.find_element_by_xpath(f'//*[@id="searchtable"]/tbody/tr[{i}]/td[2]').text
									isin = row.find_element_by_xpath(f'//*[@id="searchtable"]/tbody/tr[{i}]/td[5]').text
									found = True
									break
								i+=1
							if(found == False):
								sym_index = symbol.find(':')
								symbol = symbol[sym_index+1:]
						except:
							sym_index = symbol.find(':')
							symbol = symbol[sym_index+1:]
					if(',' in name):
						count = name.count(',')
						name = list(name)
						for i in range(count):
							name.remove(',')
						name = ''.join(name)
					ticker_list.append(symbol)
					name_list.append(name)
					isin_list.append(isin)
					
				except:
					print(f"Could not find {cusip}")
					
					cusip_to_remove.append(cusip)
					
					with open('failed_ticker_searches.csv', mode='a+',newline='') as ticker_file:
						ticker_writer = csv.writer(ticker_file, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
						ticker_writer.writerow([cusip, file_path])
			print(cusip_list)
			for cusip in  cusip_to_remove:
				cusip_list.remove(cusip)
			print(ticker_list)
			print(name_list)
			print(isin_list)

			with open('ticker_list.csv', mode='a+',newline='') as ticker_file:
				ticker_writer = csv.writer(ticker_file, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
				for i in range(0,len(ticker_list)):
					ticker_writer.writerow([ticker_list[i], name_list[i], cusip_list[i], isin_list[i]])

			driver.close()
			time.sleep(5)

def get_all_stock_files():
	main_dir = f'.\\13F_filings\\13F_Summary'
	for hedge_dir in os.listdir(main_dir):
		parent = os.path.join(main_dir, hedge_dir)
		for file in os.listdir(parent):
			file_path = os.path.join(parent,file)
			print(file_path)
			ticker_lookup(file_path)
			


def get_holdings_info(cik_to_check, date_to_check):
	main_dir = f'.\\13F_filings\\13F_Summary'
	for hedge_dir in os.listdir(main_dir):
		parent = os.path.join(main_dir, hedge_dir)
		for file in os.listdir(parent):
			file_path = os.path.join(parent,file)
			print(file)
			date = file[0:10]
			cik = file[11:21]
			if(date == date_to_check and cik == cik_to_check):
				with open(file_path, mode='r') as file:
					csv_reader = csv.reader(file)
					cusip_list = []
					value_list = []
					shares_list = []
					for row in csv_reader:
							cusip_list.append(row[1])
							value_list.append(row[2])
							shares_list.append(row[3])
							print(row)
	return(cusip_list, value_list, shares_list)
							

if __name__== "__main__":
	#get_all_stock_files()
	sql_functions.insert_stock_sql()

	#cusip, share, value = get_holdings_info('0001649339','2020-09-30')
	#print(len(cusip), len(share), len(value))

	# DRIVER_PATH = 'C:/Programming/chromedriver.exe'
	# driver = webdriver.Chrome(executable_path=DRIVER_PATH)
	# driver.get('https://stockmarketmba.com/symbollookupusingidentifier.php')
	# time.sleep(1)
	# cusip = '067901108'
	# driver.find_element_by_xpath('//*[@id="search"]').send_keys(f'{cusip}\n')
	
	# body = driver.find_element_by_tag_name('tbody')
	# rows = body.find_elements_by_tag_name('tr')
	# i=1
	# for row in rows:
	# 	country = row.find_element_by_xpath(f'//*[@id="searchtable"]/tbody/tr[{i}]/td[4]')
		
	# 	if(country.text = 'USA'):
	# 		symbol = row.find_element_by_xpath(f'//*[@id="searchtable"]/tbody/tr[{i}]/td[1]').text
	# 		name = row.find_element_by_xpath(f'//*[@id="searchtable"]/tbody/tr[{i}]/td[2]').text
	# 		isin = row.find_element_by_xpath(f'//*[@id="searchtable"]/tbody/tr[{i}]/td[5]').text
	# 	i+=1
		# //*[@id="searchtable"]/tbody/tr[1]
		# //*[@id="searchtable"]/tbody/tr[1]/td[4]
		# //*[@id="searchtable"]/tbody/tr[2]/td[4]
