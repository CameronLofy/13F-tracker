from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import os



def parse_page(url):
	time.sleep(1)
	page = requests.get(url)
	html_txt = page.text
	soup = BeautifulSoup(html_txt, 'lxml')
	

	hedge_cik = soup.find('cik').get_text()

	file_date = soup.find('periodofreport').get_text()
	file_date = file_date[6:] + '-' + file_date[0:5]
	company_name = soup.find('filingmanager').find('name').get_text().replace(' ', '_')
	company_name = hedge_cik + '_' + company_name

	name_html = soup.find_all("nameofissuer")
	cusip_html = soup.find_all("cusip")
	value_html = soup.find_all("value")
	shares_html = soup.find_all("sshprnamt")
	name = []
	cusip = []
	value = []
	shares = []

	for i in range(len(name_html)):
		name.append(name_html[i].get_text())
		cusip.append(cusip_html[i].get_text())
		value.append(value_html[i].get_text())
		shares.append(shares_html[i].get_text())
	
	df = pd.DataFrame({'Name of Issuer':name,'CUSIP':cusip, 'Value':value,'Shares':shares}) 
	#print(df)
	#print(df.loc[1, "Name of Issuer"])
	outdir = f'./13F_filings/13F_Raw/{company_name}'
	outname = f'{file_date}_{company_name}_(unedited).csv'
	if not os.path.exists(outdir):
		os.mkdir(outdir)
	full_name = os.path.join(outdir, outname)
	df.to_csv(full_name, index=False, encoding='utf-8')


	j=0
	for i in range(len(df)):
		df.loc[i, "Value"] = int(df.loc[i, "Value"].replace(',', ''))
		df.loc[i, "Shares"] = int(df.loc[i, "Shares"].replace(',', ''))
	#print(df["Value"])

	df_2 = df.iloc[:1]
	#print(df_2)

	for i in range(1,len(df)):
		if(df.iloc[i]["CUSIP"] == df.iloc[i-1]["CUSIP"]):
			# add rows together
			df_2.loc[j, "Value"] += int(df.loc[i, "Value"])
			df_2.loc[j, "Shares"] += df.loc[i, "Shares"]
		else:
			j+=1
			df_2.loc[j,"Name of Issuer"] = df.loc[i,"Name of Issuer"]
			df_2.loc[j,"CUSIP"] = df.loc[i,"CUSIP"]
			df_2.loc[j,"Value"] = df.loc[i,"Value"]
			df_2.loc[j,"Shares"] = df.loc[i,"Shares"]
	#print(df_2)
	value_sum = df_2["Value"].sum(axis = 0)
	#print(value_sum)

	ratio_list = []
	for i in range(len(df_2)):
		ratio_list.append(float((float(df_2.loc[i, "Value"]))/value_sum))
	#print(ratio_list)
	df_2.insert(4, "Ratio", ratio_list, True)
	print(df_2)
	df_2.sort_values(by=['Value'])
	print(df_2)

	outdir = f'./13F_filings/13F_Summary/{company_name}'
	outname = f'{file_date}_{company_name}_(edited).csv'
	if not os.path.exists(outdir):
		os.mkdir(outdir)
	full_name = os.path.join(outdir, outname)
	df_2.to_csv(full_name, index=False, encoding='utf-8')
	# #print(stock_list)
	return df_2
		
	

if __name__== "__main__":
	#print("starting function")
	#print(parse_page('https://www.sec.gov/Archives/edgar/data/1067983/000095012320009058/xslForm13F_X01/960.xml'))
	print(parse_page('https://www.sec.gov/Archives/edgar/data/1079114/000117266120001844/0001172661-20-001844.txt'))
	
# 	for i in range(3):
# 		print(data1[i].get_text())
# 		stock.append(data1[i].get_text())
# 	for i in range(2):
# 		print(data2[i].get_text())
# 		stock.append(data2[i].get_text())

# 	stock_list.append(stock)
# print(stock_list)
	#print(x)
# td_list =[]
# for data in tr_list:
# 	data_list = data.find_all('td')
# 	for item in data_list:
# 		print(item[0].get_text())
# 	if(('FormText' or 'FormTextR') in data_list):
# 		td_list.append(data_list)
#print(td_list)

# for seg in td_list:
# 	print(seg)
#print(td_list)
	

