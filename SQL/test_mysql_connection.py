import mysql.connector
import datetime
import csv

cnx = mysql.connector.connect(user='camlofy', password='FUnnyMAN97',
                              host='127.0.0.1',
                              database='test_hedgetracker')

cursor = cnx.cursor()

query = ("SELECT * FROM form")

cursor.execute(query)

for (form_id, hedge_id, f_type, f_date, period) in cursor:
	print(form_id, hedge_id, f_type, f_date, period)

with open('C:/Programming/HedgeFundTracker/ticker_list.csv', mode='r') as ticker_file:
	ticker_reader = csv.reader(ticker_file)
	count = 0
	for row in ticker_reader:
		if(count == 0):
			count+=1
			continue
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