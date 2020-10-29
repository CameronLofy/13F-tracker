from bs4 import BeautifulSoup
import requests
import pandas as pd
import time



def parse_page(url):
	time.sleep(1)
	page = requests.get(url)
	html_txt = page.text
	soup = BeautifulSoup(page.content, 'html.parser')
	#print(soup.prettify())

	tr_list = soup.find_all('tr')
	#print(tr_list)

	stock_list = []

	name=[]
	cusip=[]
	value=[]
	shares=[]
	total_data1 = []
	total_data2 = []
	for i in tr_list:
		stock = []
		data1 = i.find_all('td', class_="FormData")
		data2 = i.find_all('td', class_="FormDataR")
		total_data1.append(data1)
		total_data2.append(data2)
	total_data_clean1 = [x for x in total_data1 if x != []]
	total_data_clean2 = [x for x in total_data2 if x != []]

	for i in range(len(total_data_clean1)):
		name.append(total_data_clean1[i][0].get_text())
		cusip.append(total_data_clean1[i][2].get_text())
		value.append(total_data_clean2[i][0].get_text())
		shares.append(total_data_clean2[i][1].get_text())
	
	df = pd.DataFrame({'Name of Issuer':name,'CUSIP':cusip, 'Value':value,'Shares':shares}) 
	df.to_csv('greenlight_capitol.csv', index=False, encoding='utf-8')
	
	j=0
	
	for i in range(len(df)):
		df.loc[i, "Value"] = int(df.loc[i, "Value"].replace(',', ''))
		df.loc[i, "Shares"] = int(df.loc[i, "Shares"].replace(',', ''))
	print(df["Value"])

	df_2 = df.iloc[:1]
	print(df_2)

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
	print(df_2)
	value_sum = df_2["Value"].sum(axis = 0)
	print(value_sum)

	ratio_list = []
	for i in range(len(df_2)):
		ratio_list.append(float((float(df_2.loc[i, "Value"]))/value_sum))
	print(ratio_list)
	df_2.insert(4, "Ratio", ratio_list, True)

	df_2.to_csv('compact_greenlight_capitol.csv', index=False, encoding='utf-8')
	# #print(stock_list)
	return df_2
		
	

if __name__== "__main__":
	#print("starting function")
	#print(parse_page('https://www.sec.gov/Archives/edgar/data/1067983/000095012320009058/xslForm13F_X01/960.xml'))
	print(parse_page('https://www.sec.gov/Archives/edgar/data/1079114/000117266120001844/xslForm13F_X01/infotable.xml'))
	
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
	

