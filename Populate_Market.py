import mysql.connector
import yfinance as yf
import datetime
from random import randint, randrange

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

try: 
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
        "MMM": "3M Company"
    }

    # date_formated = datetime.datetime.now().strftime("%Y-%m-%d")

    # print(date_formated)

    start_date = '2015-04-23'
    end_date = '2015-05-28'
    # end_date = date_formated

    df_dict = {}
    cursor = conn.cursor(buffered=True)
    
    for tag,company in dow_jones_companies.items():

        stock_id= generate_unique_stock_id(cursor) 
        query = "SELECT Stock_id FROM Stocks WHERE Symbol = %s"
        cursor.execute(query, (tag,))
        
        existing = cursor.fetchone()
        date=start_date

        if existing is not None:
            query = "SELECT MAX(Date) FROM Stocks WHERE Symbol = %s GROUP BY Symbol;"
            cursor.execute(query, (tag,))
            res=cursor.fetchone()
            if res is not None:
                date=res[0]

        df_dict[company] =  yf.download(tag, start=date, end=end_date)
        df=df_dict[company]

        for index, row in df.iterrows():
            print(f"Date: {index.date()}, Close: {row['Close']}")

            query = "SELECT * FROM Stocks WHERE Stock_id=%s AND Date = %s AND Symbol = %s;"
            cursor.execute(query, (stock_id,index.date(), tag))
            res = cursor.fetchone()
            print(stock_id)
            if res is None:
                insert_query = "INSERT INTO Stocks (Stock_id, Symbol, Name, Date, Price, Country) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(insert_query, (stock_id, tag, company, index.date(), row['Close'], "USA"))






    # MF_dict = {
    #     "UMPIX": "ProFunds UltraMid Cap Fund",
    #     "UMPSX": "ProFunds UltraMid Cap Fund",
    #     "BIPIX": "ProFunds Biotechnology UltraSector Fund",
    #     "BIPSX": "ProFunds Biotechnology UltraSector Fund",
    #     "BRSVX": "Bridgeway Small-Cap Value",
    #     "QSMLX": "AQR Small Cap Multi-Style I",
    #     "QSERX": "AQR Small Cap Multi-Style R6",
    #     "QSMNX": "AQR Small Cap Multi-Style N",
    #     "MMEYX": "Victory Integrity Discovery Y",
    #     "MMECX": "Victory Integrity Discovery C",
    #     "MMEAX": "Victory Integrity Discovery A",
    #     "MMMMX": "Victory Integrity Discovery Member",
    #     "WBVNX": "William Blair Small Cap Value N",
    #     "ICSCX": "William Blair Small Cap Value I",
    #     "WBVRX": "William Blair Small Cap Value R6",
    #     "AXVNX": "Acclivity Small Cap Value N",
    #     "AXVIX": "Acclivity Small Cap Value I",
    #     "JMCRX": "James Micro Cap",
    #     "VFPIX": "Private Capital Management Value Fund",
    #     "VTMSX": "Vanguard Tax-Managed Small Cap Adm",
    #     "VTSIX": "Vanguard Tax-Managed Small Cap I",
    #     "RYPMX": "Rydex Precious Metals Inv",
    #     "RYZCX": "Rydex Precious Metals C",
    #     "RYMPX": "Rydex Precious Metals H",
    #     "RYMNX": "Rydex Precious Metals A"
    # }

    MF_dict = {
        "UMPIX": "ProFunds UltraMid Cap Fund"
    }

    df_dict = {}
    cursor = conn.cursor(buffered=True)
    
    for tag,company in MF_dict.items():

        MF_id= generate_unique_MF_id(cursor) 
        query = "SELECT MF_id FROM Mutual_Funds WHERE Symbol = %s"
        cursor.execute(query, (tag,))
        
        existing = cursor.fetchone()
        date=start_date

        if existing is not None:
            query = "SELECT  MAX(Date) FROM Mutual_Funds WHERE Symbol = %s GROUP BY Symbol;"
            cursor.execute(query, (tag,))
            res=cursor.fetchone()
            if res is not None:
                date=res[0]
        df_dict[company] =  yf.download(tag, start=date, end=end_date)
        df=df_dict[company]

        for index, row in df.iterrows():
            print(f"Date: {index.date()}, Close: {row['Close']}")

            query = "SELECT * FROM Mutual_Funds WHERE MF_id=%s AND Date = %s AND Symbol = %s;"
            cursor.execute(query, (MF_id,index.date(), tag))
            res = cursor.fetchone()
            print(MF_id)
            if res is None:
                insert_query = "INSERT INTO Mutual_Funds (MF_id, Symbol, Name, Date, Price, Country) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(insert_query, (MF_id, tag, company, index.date(), row['Close'], "USA"))





    # Commodity={
    #     "GC=F" : "Gold",
    #     "CL=F" : "Crude Oil",
    #     "INR=X" : "Indian Rupee",
    #     "SI=F" : "Silver",
    #     "NG=F" : "Natural Gas",
    # }

    Commodity={
        "GC=F" : "Gold"
    }

    df_dict = {}
    cursor = conn.cursor(buffered=True)
    
    for tag,company in Commodity.items():

        comm_id= generate_unique_Comm_id(cursor)
        
        existing = cursor.fetchone()
        date=start_date

        if existing is not None:
            query = "SELECT  MAX(Date) FROM Commodity WHERE Symbol = %s GROUP BY Symbol;"
            cursor.execute(query, (tag,))
            res=cursor.fetchone()
            if res is not None:
                date=res[0]
        df_dict[company] =  yf.download(tag, start=date, end=end_date)
        df=df_dict[company]

        for index, row in df.iterrows():
            print(f"Date: {index.date()}, Close: {row['Close']}")

            query = "SELECT * FROM Commodity WHERE commodity_id=%s AND Date = %s AND Symbol = %s;"
            cursor.execute(query, (comm_id,index.date(), tag))
            res = cursor.fetchone()
            print(comm_id)
            if res is None:
                insert_query = "INSERT INTO Commodity (commodity_id, Symbol, Name, Date, Price, Country) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(insert_query, (comm_id, tag, company, index.date(), row['Close'], "USA"))

    conn.commit()


except mysql.connector.Error as err:
   print(f"MySQL Error: {err}")