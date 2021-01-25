import mysql.connector
import datetime
import csv

def test_insert():
	cnx = mysql.connector.connect(user='root', password='FUnnyMAN97',
	                              host='127.0.0.1',
	                              database='test_hedgetracker')

	cursor = cnx.cursor()

	query = ("SELECT * FROM form")

	cursor.execute(query)

	for (form_id, hedge_id, f_type, f_date, period) in cursor:
		print(form_id, hedge_id, f_type, f_date, period)

	with open('C:/Programming/HedgeFundTracker/ticker_list.csv', mode='r') as ticker_file:
		ticker_reader = csv.reader(ticker_file)
		for row in ticker_reader:
			ticker = row[0]
			name = row[1]
			cusip = row[2]
			isin = row[3]

			print(ticker, name, cusip, isin)

			

			stock_query = (f"SELECT COUNT(*) FROM stock WHERE CUSIP = '{cusip}'")

			cursor.execute(stock_query)

			for x in cursor:
				if(x[0]>0):
					print("Stock already exists")

				else:
					print(f"Adding {cusip} to stock table...")
					
					#### Insert sql function here ###
					insert_stock_query = (f"INSERT INTO `test_hedgetracker`.`stock` VALUES ('{cusip}', '{name}', '{ticker}', '{isin}')")
					cursor.execute(insert_stock_query)


	with open('C:/Programming/HedgeFundTracker/failed_ticker_searches.csv', mode='r') as ticker_file:
		ticker_reader = csv.reader(ticker_file)
		for row in ticker_reader:
			cusip = row[0]
			file_path = row[1]
			print(cusip, file_path)


			with open('C:/Programming/HedgeFundTracker/'+file_path[1:]) as stock_file:
				stock_reader = csv.reader(stock_file)
				for stock_row in stock_reader:
					if(cusip == stock_row[1]):
						print(stock_row)
						print(f"inserting failed stock: {cusip}, {stock_row[0]}")
						insert_failed_stock_query = (f"INSERT INTO `test_hedgetracker`.`stock` VALUES ('{cusip}', '{stock_row[0]}', NULL, NULL)")
						cursor.execute(insert_failed_stock_query)



	cnx.commit()

	cursor.close()



	cnx.close()

def insert_stock_sql():
	# cnx = mysql.connector.connect(user='root', password='FUnnyMAN97',
	#                               host='127.0.0.1',
	#                               database='test_hedgetracker')
	cnx = mysql.connector.connect(user='camlofy', password='FUnnyMAN97',
	                              host='database-1.criu5ttpvtnp.us-west-1.rds.amazonaws.com', port='3306',
	                              database='test_hedgetracker')
	cursor = cnx.cursor()
	with open('C:/Programming/HedgeFundTracker/ticker_list.csv', mode='r') as ticker_file:
		ticker_reader = csv.reader(ticker_file)
		for row in ticker_reader:
			ticker = row[0]
			name = row[1]
			cusip = row[2]
			isin = row[3]
			cusip = cusip.zfill(9)
			print(ticker, name, cusip, isin)

			

			stock_query = (f"SELECT COUNT(*) FROM stock WHERE CUSIP = '{cusip}'")

			cursor.execute(stock_query)

			for x in cursor:
				if(x[0]>0):
					print("Stock already exists")

				else:
					print(f"Adding {cusip} to stock table...")
					
					#### Insert sql function here ###
					insert_stock_query = (f"INSERT INTO `test_hedgetracker`.`stock` VALUES ('{cusip}', '{name}', '{ticker}', '{isin}')")
					cursor.execute(insert_stock_query)

	cnx.commit()

	cursor.close()



	cnx.close()


def insert_hedge_sql(hedge_id, hedge_name):
	cnx = mysql.connector.connect(user='camlofy', password='FUnnyMAN97',
	                              host='database-1.criu5ttpvtnp.us-west-1.rds.amazonaws.com', port='3306',
	                              database='test_hedgetracker')


	cursor = cnx.cursor()
	check_query = (f"SELECT COUNT(*) FROM hedge_fund WHERE hedge_id = '{hedge_id}'")

	cursor.execute(check_query)

	for x in cursor:
		if(x[0]>0):
			print("Hedge fund already exists")

		else:
			print(f"Inserting {hedge_name} ({hedge_id}) into table...")
			query = (f"INSERT INTO `test_hedgetracker`.`hedge_fund` VALUES ('{hedge_id}', '{hedge_name}')")
			cursor.execute(query)
	cnx.commit()

	cursor.close()



	cnx.close()

	
def insert_form_sql(form_id, hedge_id, file_type, file_date, period_date):
	cnx = mysql.connector.connect(user='root', password='FUnnyMAN97',
	                              host='127.0.0.1',
	                              database='test_hedgetracker')

	cursor = cnx.cursor()
	check_query = (f"SELECT COUNT(*) FROM form WHERE form_id = '{form_id}'")

	cursor.execute(check_query)

	for x in cursor:
		if(x[0]>0):
			print("Form already exists")

		else:
			print(f"Inserting {file_type} ({form_id}) into table...")
			query = (f"INSERT INTO `test_hedgetracker`.`form` VALUES ('{form_id}', '{hedge_id}', '{file_type}', '{file_date}', '{period_date}')")
			cursor.execute(query)
	cnx.commit()

	cursor.close()



	cnx.close()

def insert_holdings_sql(form_id, hedge_id, cusip, shares, value):
	cnx = mysql.connector.connect(user='root', password='FUnnyMAN97',
	                              host='127.0.0.1',
	                              database='test_hedgetracker')

	cursor = cnx.cursor()
	check_query = (f"SELECT COUNT(*) FROM holdings WHERE form_id = '{form_id}' AND cusip = '{cusip}'")

	cursor.execute(check_query)

	for x in cursor:
		if(x[0]>0):
			print("Stock holding already exists")

		else:
			print(f"Inserting {cusip} ({form_id}) into table...")
			query = (f"INSERT INTO `test_hedgetracker`.`holdings` VALUES ('{form_id}-{cusip}', '{form_id}', '{hedge_id}', '{cusip}', '{shares}', '{value}')")
			cursor.execute(query)
	cnx.commit()

	cursor.close()



	cnx.close()

def get_change_sql(hedge_id):
	cnx = mysql.connector.connect(user='camlofy', password='FUnnyMAN97',
	                              host='database-1.criu5ttpvtnp.us-west-1.rds.amazonaws.com', database='test_hedgetracker')

	cursor = cnx.cursor()

	date_query = ("SELECT form.period "+
		"FROM form, hedge_fund "+
		f"WHERE form.hedge_id = {hedge_id} AND form.hedge_id = hedge_fund.hedge_id "+
		"ORDER BY form.period DESC LIMIT 2")
	cursor.execute(date_query)
	form_dates = []
	for period in cursor:
		form_dates.append(period[0])

	
	stock_list_1 = []
	stock_list_2 = []
	for form_date in form_dates:
		print(form_date)
		holdings_query = (f"SELECT hedge.hedge_id, s.s_name, s.ticker, h.shares, h.value "+
			"FROM holdings as h "+
			"JOIN hedge_fund as hedge "+
			"ON h.hedge_id = hedge.hedge_id "+
			"JOIN stock as s ON s.cusip = h.cusip "+
			"WHERE form_id = "+
				"(SELECT form_id FROM form "+
				f"WHERE form.hedge_id = {hedge_id} AND form.period = '{form_date}') "+
			"ORDER BY s.ticker ASC")

		cursor.execute(holdings_query)
		if(form_date == form_dates[0]):
			for row in cursor:
				stock_list_1.append(row)
		else:
			for row in cursor:
				stock_list_2.append(row)
	print(stock_list_1)
	print(stock_list_2)

	final_stock_list = []


	i,j=0,0
	
	while(i<len(stock_list_1) and j<len(stock_list_2)):
		stock_row = []
		if(stock_list_1[i][2] == stock_list_2[j][2]):
			print(stock_list_1[i][2])
			print("Changed value")


			for n in range(5):
				stock_row.append(stock_list_1[i][n])
			diff = stock_list_1[i][3] - stock_list_2[j][3]
			if(diff>0):
				stock_row.append(diff)
				stock_row.append('bought')
			elif(diff<0):
				stock_row.append(-diff)
				stock_row.append('sold')
			else:
				stock_row.append(0)
				stock_row.append('no change')

			i+=1
			j+=1
		
		elif(stock_list_1[i][2] < stock_list_2[j][2]):
			print(stock_list_1[i][2])
			print("Bought All New")
			for n in range(5):
				stock_row.append(stock_list_1[i][n])
			stock_row.append(stock_list_1[i][3])
			stock_row.append("Bought All New")
			i+=1

		elif(stock_list_1[i][2] > stock_list_2[j][2]):
			print(stock_list_2[j][2])
			print("Sold All")
			for n in range(3):
				stock_row.append(stock_list_2[j][n])
			stock_row.append(0)
			stock_row.append("Sold All")

			j+=1
		print(f"i: {i}")
		print(f"j: {j}")
		final_stock_list.append(stock_row)
		

	while(i<len(stock_list_1)):
		stock_row=[]
		print(stock_list_1[i][2])
		print("Bought All New")
		for n in range(5):
			stock_row.append(stock_list_1[i][n])
		stock_row.append(stock_list_1[i][3])
		stock_row.append("Bought All New")
		i+=1
		final_stock_list.append(stock_row)

	while(j<len(stock_list_2)):
		stock_row=[]
		print(stock_list_2[j][2])
		print("Sold All")
		for n in range(3):
			stock_row.append(stock_list_2[j][n])
		stock_row.append(0)
		stock_row.append("Sold All")
		j+=1
		final_stock_list.append(stock_row)

	for row in final_stock_list:
		print(row)
	cursor.close()
	cnx.close()

if __name__== "__main__":
	cnx = mysql.connector.connect(user='camlofy', password='FUnnyMAN97',
	                              host='database-1.criu5ttpvtnp.us-west-1.rds.amazonaws.com')

	cursor = cnx.cursor()

	query = ("SELECT User, Host from mysql.user")

	cursor.execute(query)
	for (user, host) in cursor:
		print(user, host)
	cursor.close()
	cnx.close()

	get_change_sql('1067983')
	# hedge_id_list = ['0001067983', '0001096343', '0001166559', '0001079114', '0001649339', '0001336528']
	# hedge_name_list = ['BERKSHIRE HATHAWAY INC', 'MARKEL CORP', 'BILL & MELINDA GATES FOUNDATION TRUST', 'GREENLIGHT CAPITAL INC', 'Scion Asset Management, LLC', 'Pershing Square Capital Management, L.P.']
	# for i in range(len(hedge_id_list)):
	# 	insert_hedge_sql(hedge_id_list[i], hedge_name_list[i])