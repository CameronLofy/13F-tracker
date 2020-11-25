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
	cnx = mysql.connector.connect(user='root', password='FUnnyMAN97',
	                              host='127.0.0.1',
	                              database='test_hedgetracker')
	cursor = cnx.cursor()
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

	cnx.commit()

	cursor.close()



	cnx.close()


def insert_hedge_sql(hedge_id, hedge_name):
	cnx = mysql.connector.connect(user='root', password='FUnnyMAN97',
	                              host='127.0.0.1',
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

def insert_holdings_sql(csv_file):
	print('Finish code here')