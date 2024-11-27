import mysql.connector
import datetime
from random import randint, randrange
import requests

def generate_unique_stock_id(cursor):
    stock_id = None
    while stock_id is None:
        temp_id = randint(0, 999999)
        query = "SELECT Stock_id FROM Stocks WHERE Stock_id = %s"
        cursor.execute(query, (temp_id,))
        result = cursor.fetchone()

        if result is None:
            stock_id = temp_id
    return stock_id

def generate_unique_MF_id(cursor):
    MF_id = None
    while MF_id is None:
        temp_id = randint(0, 999999)
        query = "SELECT MF_id FROM Mutual_Funds WHERE MF_id = %s"
        cursor.execute(query, (temp_id,))
        result = cursor.fetchone()

        if result is None:
            MF_id = temp_id
    return MF_id

def generate_unique_Comm_id(cursor):
    comm_id = None
    while comm_id is None:
        temp_id = randint(0, 999999)
        query = "SELECT commodity_id FROM Commodity WHERE commodity_id = %s"
        cursor.execute(query, (temp_id,))
        result = cursor.fetchone()

        if result is None:
            comm_id = temp_id
    return comm_id


conn= mysql.connector.connect(host= 'localhost',user= 'root',password= '@Aditya171')
if conn.is_connected():
    print("SQL Connected")

create_db_query = "CREATE DATABASE IF NOT EXISTS Market;"
cursor = conn.cursor()
cursor.execute(create_db_query)
conn.commit()
conn.close()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Aditya171",
    database="Market"
)

# dow_jones_companies = {
#     "MMM": "3M Company",
#     "AXP": "American Express",
#     "AMGN": "Amgen Inc.",
#     "AAPL": "Apple Inc.",
#     "BA": "Boeing",
#     "CAT": "Caterpillar Inc.",
#     "CVX": "Chevron Corporation",
#     "CSCO": "Cisco Systems",
#     "KO": "The Coca-Cola Company",
#     "DOW": "Dow Inc.",
#     "GS": "Goldman Sachs",
#     "HD": "The Home Depot",
#     "HON": "Honeywell",
#     "IBM": "IBM",
#     "INTC": "Intel Corporation",
#     "JNJ": "Johnson & Johnson",
#     "JPM": "JPMorgan Chase & Co.",
#     "MCD": "McDonald's Corp.",
#     "MRK": "Merck & Co., Inc.",
#     "MSFT": "Microsoft Corp.",
#     "NKE": "Nike, Inc.",
#     "PG": "Procter & Gamble",
#     "CRM": "Salesforce.com",
#     "TRV": "The Travelers Companies Inc.",
#     "UNH": "UnitedHealth Group Inc.",
#     "VZ": "Verizon",
#     "V": "Visa Inc.",
#     "WMT": "Walmart Inc.",
#     "DIS": "Walt Disney Company",
#     "WBA": "Walgreens Boots Alliance, Inc."
# }

dow_jones_companies = {
    "AAPL": "Apple"
}

start_date = '2023-04-23'
end_date = '2023-05-28'
api_key = "oCy2CTEcIxntCZD6oJUT0lGqWN79arQZ"

# df_dict = {}
cursor = conn.cursor(buffered=True)

for tag, company in dow_jones_companies.items():
    stock_id = generate_unique_stock_id(cursor)

    # Check if stock already exists in the database
    query = "SELECT Stock_id FROM Stocks WHERE Symbol = %s"
    cursor.execute(query, (tag,))
    existing = cursor.fetchone()
    date = start_date

    if existing is not None:
        query = "SELECT MAX(Date) FROM Stocks WHERE Symbol = %s GROUP BY Symbol;"
        cursor.execute(query, (tag,))
        res = cursor.fetchone()
        if res is not None:
            date = res[0].strftime("%Y-%m-%d")


    # Call the Polygon API to fetch stock data
    url = f"https://api.polygon.io/v2/aggs/ticker/{tag}/range/1/day/{date}/{end_date}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "apiKey": api_key
    }

    print(requests)
    url= f"https://api.polygon.io/v2/aggs/ticker/{tag}/range/1/day/{date}/{end_date}?adjusted=true&sort=asc&apiKey=mhIlvMZM2os4PNooKe75Pkcp4VNIUek8"
    print(url)
    response = requests.get(url)
    # response = requests.get(url, params=params)
    print(response)
    if response.status_code == 200:
        stock_data = response.json().get("results", [])

        for entry in stock_data:
            close_price = entry['c']
            timestamp = entry['t']
            date_str = datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')

            print(f"Date: {date_str}, Close: {close_price}")

            # Check if the entry already exists in the database
            query = "SELECT * FROM Stocks WHERE Stock_id=%s AND Date = %s AND Symbol = %s;"
            cursor.execute(query, (stock_id, date_str, tag))
            res = cursor.fetchone()
            
            if res is None:
                insert_query = """
                    INSERT INTO Stocks (Stock_id, Symbol, Name, Date, Price)
                    VALUES (%s, %s, %s, %s, %s);
                """
                cursor.execute(insert_query, (stock_id, tag, company, date_str, close_price))
                print(f"Inserted data for {company} on {date_str} with close price {close_price}")
    else:
        print(f"Failed to fetch data for {company} ({tag}). Status code: {response.status_code}")

# Commit transactions after insertion
conn.commit()

query = "SELECT * FROM Stocks"
cursor.execute(query)
res = cursor.fetchall()
print(res)




MF_dict = {
    "Birla Sun Life Fixed Term Plan - Series AD - RETAIL DIVIDEND": 106986
}

start_date = '2023-04-23'
end_date = '2023-05-28'
# api_key = "oCy2CTEcIxntCZD6oJUT0lGqWN79arQZ"

df_dict = {}
cursor = conn.cursor(buffered=True)

for company, code in MF_dict.items():

    # Check if stock already exists in the database
    query = "SELECT MF_id FROM Mutual_Funds WHERE Name = %s"
    cursor.execute(query, (company,))
    existing = cursor.fetchone()
    date = start_date

    if existing is not None:
        query = "SELECT MAX(Date) FROM Mutual_Funds WHERE Name = %s GROUP BY Name;"
        cursor.execute(query, (company,))
        res = cursor.fetchone()
        if res is not None:
            date = res[0].strftime("%Y-%m-%d")


    # Call the MF API to fetch MF data
    url = f"https://api.mfapi.in/mf/{code}"
    
    response = requests.get(url)
    data = response.json()

    # Search for the target date in the data
    nav_data = data.get("data", [])
    print(nav_data)
    for entry in nav_data:
        # date= entry.get("date")
        date_str = datetime.datetime.strptime(entry["date"], "%d-%m-%Y").strftime("%Y-%m-%d")

        query = "SELECT * FROM Mutual_Funds WHERE MF_id=%s AND Date = %s;"
        cursor.execute(query, (code, date_str))
        res = cursor.fetchone()

        price= entry.get("nav")
        
        if res is None:
            insert_query = """
                INSERT INTO Mutual_Funds (MF_id, Name, Date, nav)
                VALUES (%s, %s, %s, %s);
            """
            cursor.execute(insert_query, (code, company, date_str, price))
            print(f"Inserted data for {company} on {date_str} with close price {price}")
        else:
            print(f"Failed to fetch data for {company} ({code}). Status code: {response.status_code}")

        # Commit transactions after insertion
        conn.commit()



# Commodity={
#     "GC=F" : "Gold",
#     "CL=F" : "Crude Oil",
#     "INR=X" : "Indian Rupee",
#     "SI=F" : "Silver",
#     "NG=F" : "Natural Gas",
# }

# https://api.polygon.io/v2/aggs/ticker/C:USDINR/range/1/day/2023-01-09/2023-01-09?apiKey=mhIlvMZM2os4PNooKe75Pkcp4VNIUek8


# df_dict = {}
# cursor = conn.cursor(buffered=True)

# for tag,company in Commodity.items():

#     comm_id= generate_unique_Comm_id(cursor)
    
#     existing = cursor.fetchone()
#     date=start_date

#     if existing is not None:
#         query = "SELECT  MAX(Date) FROM Commodity WHERE Symbol = %s GROUP BY Symbol;"
#         cursor.execute(query, (tag,))
#         res=cursor.fetchone()
#         if res is not None:
#             date=res[0]
#     df_dict[company] =  yf.download(tag, start=date, end=end_date)
#     df=df_dict[company]

#     for index, row in df.iterrows():
#         print(f"Date: {index.date()}, Close: {row['Close']}")

#         query = "SELECT * FROM Commodity WHERE commodity_id=%s AND Date = %s AND Symbol = %s;"
#         cursor.execute(query, (comm_id,index.date(), tag))
#         res = cursor.fetchone()
#         print(comm_id)
#         if res is None:
#             insert_query = "INSERT INTO Commodity (commodity_id, Symbol, Name, Date, Price, Country) VALUES (%s, %s, %s, %s, %s, %s);"
#             cursor.execute(insert_query, (comm_id, tag, company, index.date(), row['Close'], "USA"))

# conn.commit()



start_date = '2023-04-23'
end_date = '2023-05-28'
api_key = "oCy2CTEcIxntCZD6oJUT0lGqWN79arQZ"

cursor = conn.cursor(buffered=True)

Commodity={
    "US Dollar" : "USD"
}
for Commodity, tag in Commodity.items():
    stock_id = generate_unique_Comm_id(cursor)

    # Check if stock already exists in the database
    query = "SELECT commodity_id FROM Commodity WHERE Symbol = %s"
    cursor.execute(query, (tag,))
    existing = cursor.fetchone()
    date = start_date

    if existing is not None:
        query = "SELECT MAX(Date) FROM Commodity WHERE Symbol = %s GROUP BY Symbol;"
        cursor.execute(query, (tag,))
        res = cursor.fetchone()
        if res is not None:
            date = res[0].strftime("%Y-%m-%d")


    url = f"https://api.polygon.io/v2/aggs/ticker/C:{tag}INR/range/1/day/{date}/{end_date}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "apiKey": api_key
    }

    print(requests)
    url= f"https://api.polygon.io/v2/aggs/ticker/{tag}/range/1/day/{date}/{end_date}?adjusted=true&sort=asc&apiKey=mhIlvMZM2os4PNooKe75Pkcp4VNIUek8"
    print(url)
    response = requests.get(url)
    # response = requests.get(url, params=params)
    print(response)
    if response.status_code == 200:
        stock_data = response.json().get("results", [])

        for entry in stock_data:
            close_price = entry['c']
            timestamp = entry['t']
            date_str = datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')

            print(f"Date: {date_str}, Close: {close_price}")

            # Check if the entry already exists in the database
            query = "SELECT * FROM Commodity WHERE Commodity_id=%s AND Date = %s AND Symbol = %s;"
            cursor.execute(query, (stock_id, date_str, tag))
            res = cursor.fetchone()
            
            if res is None:
                insert_query = """
                    INSERT INTO Commodity (Commodity_id, Symbol, Name, Date, rate)
                    VALUES (%s, %s, %s, %s, %s);
                """
                cursor.execute(insert_query, (stock_id, tag, Commodity, date_str, close_price))
                print(f"Inserted data for {Commodity} on {date_str} with close price {close_price}")
    else:
        print(f"Failed to fetch data for {Commodity} ({tag}). Status code: {response.status_code}")

# Commit transactions after insertion
conn.commit()

query = "SELECT * FROM Commodity"
cursor.execute(query)
res = cursor.fetchall()
print(res)