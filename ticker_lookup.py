from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import csv
import os

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
		DRIVER_PATH = 'C:/Programming/chromedriver.exe'
		driver = webdriver.Chrome(executable_path=DRIVER_PATH)
		driver.get('https://stockmarketmba.com/symbollookupusingidentifier.php')
		time.sleep(1)

		if(cusip_list[0] == 'CUSIP'):
			cusip_list.remove('CUSIP')
			print(cusip_list)
		for cusip in cusip_list:
			
			driver.find_element_by_xpath('//*[@id="search"]').send_keys(f'{cusip}\n')

			time.sleep(2)
			try:
				symbol = driver.find_element_by_xpath('//*[@id="searchtable"]/tbody/tr[1]/td[1]').text
				name = driver.find_element_by_xpath('//*[@id="searchtable"]/tbody/tr/td[2]').text
				isin = driver.find_element_by_xpath('//*[@id="searchtable"]/tbody/tr/td[5]').text
				if(':' in symbol):
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
				with open('failed_ticker_searches.csv', mode='a+',newline='') as ticker_file:
					ticker_writer = csv.writer(ticker_file, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
					ticker_writer.writerow([cusip, file_path])
					cusip_list.remove(cusip)
		print(ticker_list)
		print(name_list)
		print(isin_list)

		with open('ticker_list.csv', mode='a+',newline='') as ticker_file:
			ticker_writer = csv.writer(ticker_file, delimiter=',', quotechar="'", quoting=csv.QUOTE_MINIMAL)
			for i in range(0,len(ticker_list)):
				ticker_writer.writerow([ticker_list[i], name_list[i], cusip_list[i], isin_list[i]])

	driver.close()

def get_all_stock_files():
	main_dir = f'.\\13F_filings\\13F_Summary'
	for hedge_dir in os.listdir(main_dir):
		parent = os.path.join(main_dir, hedge_dir)
		for file in os.listdir(parent):
			file_path = os.path.join(parent,file)
			print(file_path)
			ticker_lookup(file_path)

if __name__== "__main__":
	get_all_stock_files()