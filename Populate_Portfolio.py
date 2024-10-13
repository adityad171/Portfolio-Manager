import mysql.connector
import random

# Function to connect to MySQL database
def connect_to_database(db_name):
    connection = mysql.connector.connect(
        host='localhost',  # Your MySQL host
        user='root',  # Your MySQL username
        password='@Aditya171',  # Your MySQL password
        database=db_name
    )
    return connection

# Function to get 5 stock data from the 'Stocks' table in 'Market' database
def get_stocks_data(cursor):
    query = "SELECT Stock_id, Name, Price FROM Stocks WHERE Date = '2015-04-23'"
    cursor.execute(query)
    stocks_data = cursor.fetchall()
    # print(stocks_data)
    return stocks_data

# Function to insert stock data into the 'Asset' table in 'PORTFOLIOS' database
def insert_into_asset(cursor, stock_id, stock_name, purchase_price):
    portfolio_id = random.randint(1, 9999999)  # Random portfolio_id
    quantity = random.randint(1, 10)  # Random quantity
    
    insert_query = """
    INSERT INTO Asset (asset_id, portfolio_id, asset_name, asset_type, quantity, purchase_price, current_price)
    VALUES (%s, %s, %s, 'Stock', %s, %s, NULL)
    """
    values = (stock_id, portfolio_id, stock_name, quantity, purchase_price)
    
    cursor.execute(insert_query, values)

# Connect to the Market database to get stock data
market_connection = connect_to_database('Market')
market_cursor = market_connection.cursor()

# Fetch stock data for 5 stocks
stocks_data = get_stocks_data(market_cursor)
print("Stock Data:", stocks_data)

# Close Market DB connection
market_cursor.close()
market_connection.close()

# Connect to the PORTFOLIOS database to insert stock data
portfolios_connection = connect_to_database('PORTFOLIOS')
portfolios_cursor = portfolios_connection.cursor()

# Insert each stock into the Asset table
# for stock in stocks_data:
#     stock_id, stock_name, purchase_price = stock
    # insert_into_asset(portfolios_cursor, stock_id, stock_name, purchase_price)

insert_query = """
    SELECT * FROM ASSET
    """

portfolios_cursor.execute(insert_query)
existing = portfolios_cursor.fetchone()
print("data"+str(existing))

# Commit the transaction
portfolios_connection.commit()

# Close PORTFOLIOS DB connection
portfolios_cursor.close()
portfolios_connection.close()
