import jellyfish
import subprocess
from collections import Counter
import re
from datetime import datetime
import mysql.connector
from dateutil.relativedelta import relativedelta
import pandas as pd
import time
import numpy as np

# Temporary portfolio
temp_portfolio = []

def menu():
    print("1. Get analysis of your portfolio")
    print("2. Add assets")
    print("3. Remove assets")
    print("4. Create portfolio")  # New menu option
    print("5. Get top 10 assets")
    print("6. Search Asset")
    print("7. Risk Assessment of Portfolio")
    print("8. Popular Assets")
    print("9. Exit")

def choose_duration():
    print("1. 1 day")
    print("2. 1 month")
    print("3. 1 year")

def connect_to_database(database_name):
    connection = mysql.connector.connect(
        host='localhost',  # Replace with your MySQL host
        user='root',  # Replace with your MySQL username
        password='@Aditya171',  # Replace with your MySQL password
        database=database_name
    )
    cursor = connection.cursor()
    return connection, cursor

def login(username, password):
    connection, cursor = connect_to_database("USERS")
    if connection is None:
        print("Could not connect to the database.")
        return False
    
    query = f"SELECT * FROM customers WHERE customer_username = %s AND customer_password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        print("Customer found.")
        return True
    else:
        print("Invalid credentials.")
        return False
    


def buy_asset(user_id):
    global temp_portfolio

    connection, cursor = connect_to_database("Market")
    query = f"SELECT DISTINCT Name FROM Stocks"
    cursor.execute(query)

    result = cursor.fetchall()
    company_list = [row[0] for row in result]  # List comprehension for cleaner code
    company = chooseCompany(company_list, user_id)

    query = f"SELECT * FROM Stocks where Name='{company}'"
    cursor.execute(query)
    id = cursor.fetchone()[0]

    print("Enter quantity:")
    quantity = int(input())


    temp_portfolio.append({"asset_name": company, "asset_id": id, "quantity": quantity})
    print(f"Added {quantity} units of {company} to the temporary portfolio.")

    print(temp_portfolio)

def sell_asset():
    global temp_portfolio
    i = 1
    print("What do you want to sell?")
    for asset in temp_portfolio:
        print(f"{i}. {asset['asset_name']} : Quantity= {asset['quantity']}")
        i += 1

    ind = int(input("Enter index (integer only): "))
    quantity = int(input("Quantity to sell (integer only): "))
    asset_name = temp_portfolio[ind - 1]["asset_name"]

    for asset in temp_portfolio:
        if asset["asset_name"] == asset_name:
            if asset["quantity"] >= quantity:
                asset["quantity"] -= quantity
                print(f"Removed {quantity} units of {asset_name} from the temporary portfolio.")
                if asset["quantity"] == 0:
                    temp_portfolio.remove(asset)
                return
            else:
                print("Not enough quantity to sell.")
                return
    print(f"{asset_name} not found in the temporary portfolio.")

    print(temp_portfolio)

def create_portfolio(user_id):
    global temp_portfolio
    if not temp_portfolio:
        print("Temporary portfolio is empty. Nothing to save.")
        return

    connection2, cursor2 = connect_to_database("PORTFOLIOS")
    if cursor2 is None:
        print("Failed to connect to the database. Please check your database settings.")
        return

    try:
        # Fetch the user's portfolio
        query = f"SELECT * FROM PORTFOLIO WHERE user_id = '{user_id}'"
        cursor2.execute(query)
        result2 = cursor2.fetchone()
        if not result2:
            print(f"No portfolio found for user ID: {user_id}")
            return

        portfolio_id = result2[0]

        # Insert assets into the user's portfolio
        for asset in temp_portfolio:
            current_date = datetime.now().strftime("%Y-%m-%d")
            current_date= '2024-10-28'
            # Fetch current price from the Market database
            connection_market, cursor_market = connect_to_database("Market")
            query_market = f"SELECT * FROM Stocks WHERE name='{asset['asset_name']}' AND date='{current_date}'"
            cursor_market.execute(query_market)
            stock_data = cursor_market.fetchone()
            
            if not stock_data:
                print(f"Stock data for {asset['asset_name']} not found for date {current_date}.")
                continue
            
            purchase_price = stock_data[4]  # Assuming the 5th column is the price
            
            # Insert into the 'asset' table in the PORTFOLIOS database
            query_insert = (
                f"INSERT INTO asset (asset_id, portfolio_id, asset_name, asset_type, quantity, purchase_price, current_price) "
                f"VALUES ('{asset['asset_id']}', '{portfolio_id}', '{asset['asset_name']}', 'stock', {asset['quantity']}, {purchase_price}, {purchase_price});"
            )
            cursor2.execute(query_insert)

            # Close the Market database connection
            cursor_market.close()
            connection_market.close()

        connection2.commit()
        print("Portfolio saved successfully.")
        temp_portfolio.clear()  # Clear temporary portfolio after saving
    except mysql.connector.Error as err:
        print(f"Error during portfolio creation: {err}")
    finally:
        cursor2.close()
        connection2.close()

def getCustomerID(username, type= "customer"):
    connection, cursor = connect_to_database("USERS")
    if connection is None:
        print("Could not connect to the database.")
        return False
    
    # SQL query to find the customer
    query = f"SELECT * FROM {type}s WHERE {type}_username = '{username}'"
    # print(query)
    cursor.execute(query)
    
    # Fetch one result
    result = cursor.fetchone()
    # print(result)

    # Close the connection
    cursor.close()
    connection.close()

    return result[3]


def query1(user):
    connection, cursor = connect_to_database("PORTFOLIOS")
    user= int(user)
    # print(result)
    query = f"SELECT * FROM PORTFOLIO WHERE user_id = '{user}'"
    # print(query)
    cursor.execute(query)

    result = cursor.fetchone()[0]

    query = f"SELECT * FROM Asset WHERE portfolio_id = '{result}'"
    
    print(query)
    cursor.execute(query)

    result = cursor.fetchall()

    assets=0
    net=0
    # avg=0
    # temp=0

    for row in result:
        print(row)
        assets+=1
        net+=(row[4]*(row[6]-row[5]))

    print(f"number of assets: {assets}")
    print(f"Net Profit/loss: {net}")

def query5():
    choose_duration()
    dur = int(input())
    connection, cursor = connect_to_database("MARKET")
    # connection, cursor2 = connect_to_database("MARKET")

    init_date= None

    current_date = datetime.now()
    current_date= "2024-10-28"
    date_formated= "2024-10-28"
    # date_formated = current_date.strftime("%Y-%m-%d")

    if dur==1:
        # one_day_ago = current_date - relativedelta(days=1)
        # init_date = one_day_ago.strftime("%Y-%m-%d")
        init_date= "2024-10-27"
    elif dur==2:
        # one_month_ago = current_date - relativedelta(months=1)
        # init_date = one_month_ago.strftime("%Y-%m-%d")
        init_date= "2024-09-28"

    elif dur==3:
        # one_year_ago = current_date - relativedelta(years=1)
        # init_date = one_year_ago.strftime("%Y-%m-%d")
        init_date= "2023-10-28"


    query = f"SELECT * FROM STOCKS WHERE date = '{date_formated}' ORDER BY name"
    print(query)
    cursor.execute(query)

    result = cursor.fetchall()
    # print(result)

    query2 = f"SELECT * FROM STOCKS WHERE date = '{init_date}' ORDER BY name"
    print(query2)
    cursor.execute(query2)

    result2 = cursor.fetchall()
        
    # print(result2)
    dict= {}
    for row1, row2 in zip(result, result2):
        # diff = [val2 - val1 for val1, val2 in zip(row1, row2)]
        dict.update({row1[2]: (row1[4]-row2[4])})
        # print(row1)
        # print(row2)
    ans= {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=True)}
    print(dict)
    print(ans)

    top_10_items = list(ans.items())[:10]
    for i in range (min(10, len(top_10_items))):
        print(f"{i+1}. {top_10_items[i][0]}, Price:{top_10_items[i][1]}")

def query7(user):
    connection, cursor = connect_to_database("PORTFOLIOS")

    user= int(user)
    # print(result)
    query = f"SELECT * FROM PORTFOLIO WHERE user_id = '{user}'"
    # print(query)
    cursor.execute(query)

    result = cursor.fetchone()[0]
    print(result)

    query = f"SELECT * FROM Asset WHERE portfolio_id = '{result}'"
    
    print(query)
    cursor.execute(query)

    result = cursor.fetchall()
    # print(result)

    val=0
    wt=[]
    returns = []

    init_date= None

    current_date = datetime.now()
    current_date= "2024-10-28"
    connection2, cursor2 = connect_to_database("MARKET")

    for row in result:

        arr=[]
        print(row)
        temp=(row[4]*row[6])
        val+=temp
        wt.append(temp)

        # one_year_ago = current_date - relativedelta(years=1)
        # init_date = one_year_ago.strftime("%Y-%m-%d")
        init_date= "2023-10-28"
        # query2 = f"SELECT * FROM STOCKS WHERE date = '{init_date}' and Name={row[2]}"
        query2 = f"SELECT * FROM STOCKS WHERE Name='{row[2]}' and date = '{init_date}'"
        print(query2)
        cursor2.execute(query2)
        result2 = cursor2.fetchone()
        arr.append(result2[4])

        time.sleep(2)

        # six_month_ago = current_date - relativedelta(months=6)
        # init_date = six_month_ago.strftime("%Y-%m-%d")
        init_date= "2024-04-28"
        # query2 = f"SELECT * FROM STOCKS WHERE date = '{init_date}' and Name={row[2]}"
        query2 = f"SELECT * FROM STOCKS WHERE Name='{row[2]}' and date = '{init_date}'"

        print(query2)
        cursor2.execute(query2)
        result2 = cursor2.fetchone()
        arr.append(result2[4])

        time.sleep(2)

        # one_month_ago = current_date - relativedelta(months=1)
        # init_date = one_month_ago.strftime("%Y-%m-%d")
        init_date= "2024-09-28"
        # query2 = f"SELECT * FROM STOCKS WHERE date = '{init_date}' and Name={row[2]}"
        query2 = f"SELECT * FROM STOCKS WHERE Name='{row[2]}' and date = '{init_date}'"

        print(query2)
        cursor2.execute(query2)
        result2 = cursor2.fetchone()
        arr.append(result2[4])

        time.sleep(2)

        # init_date = current_date.strftime("%Y-%m-%d")
        init_date= "2024-10-28"
        # query2 = f"SELECT * FROM STOCKS WHERE date = '{init_date}' and Name={row[2]}"
        query2 = f"SELECT * FROM STOCKS WHERE Name='{row[2]}' and date = '{init_date}'"

        print(query2)
        cursor2.execute(query2)
        result2 = cursor2.fetchone()
        arr.append(result2[4])

    for i in range(len(wt)):
        wt[i]=wt[i]/val
    # Example asset returns and weights
    weights = np.array(wt)  # Portfolio weights of 3 assets
    returns = np.array(arr)

    print(weights)
    print(returns)

    # Calculate covariance matrix
    cov_matrix = np.cov(returns)

    # Portfolio variance
    portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))

    # Portfolio standard deviation (risk)
    portfolio_risk = np.sqrt(portfolio_variance)

    print(f'Portfolio Risk (Standard Deviation): {portfolio_risk:.4f}')

# Function to calculate Jaro-Winkler similarity and return top 5 closest matches
def get_top_5_closest_matches(user_input, company_list):
    # List to store company names and their similarity scores
    similarity_scores = []
    
    # Calculate Jaro-Winkler similarity between the input and each company name in the list
    for c in company_list:
        score = jellyfish.jaro_winkler_similarity(user_input, c)
        similarity_scores.append((c, score))
    
    # Sort the companies based on similarity score in descending order
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Get top 5 closest matches
    top_5_matches = similarity_scores[:5]
    
    return top_5_matches

def chooseCompany(company_list, user_id):
    print("Enter company Name: ")
    company= input()
    # Get top 5 closest matches
    top_matches = get_top_5_closest_matches(company, company_list)

    # Print the top 5 matches with their similarity scores
    print("Top 5 closest matches:")
    i=1
    for c, score in top_matches:
        if(score>0.5):
            print(f"{i}. {c}")
            i+=1
    print(f"{i}. None")
    print("Confirm the company (by entering the number):")

    connection, cursor = connect_to_database("USERS")

    current_date = datetime.now().strftime("%Y-%m-%d")
    current_date= '2024-04-24'

    confirm= int(input())
    if confirm < i and confirm>0:
        query = (f"INSERT INTO SEARCH (user_id, query, company, date) "
             f"VALUES ('{user_id}', '{company}', '{top_matches[confirm-1][0]}', '{current_date}');")
        cursor.execute(query)

    connection.commit()

    return top_matches[confirm-1][0]


def portfolio_analysis():
    global temp_portfolio

    if not temp_portfolio:
        print("The temporary portfolio is empty. Please add assets to analyze.")
        return

    connection, cursor = connect_to_database("Market")
    current_date = datetime.now().strftime("%Y-%m-%d")

    total_assets = 0
    net_profit_loss = 0

    print("Analyzing your temporary portfolio...\n")
    print(f"{'Asset Name':<15}{'Quantity':<10}{'Purchase Price':<15}{'Current Price':<15}{'Profit/Loss':<15}")
    print("-" * 70)

    for asset in temp_portfolio:
        asset_name = asset['asset_name']
        quantity = asset['quantity']
        
        # Fetch current price from the Market database
        query = f"SELECT * FROM Stocks WHERE name='{asset_name}' AND date='{current_date}'"
        cursor.execute(query)
        stock_data = cursor.fetchone()

        if not stock_data:
            print(f"Current price for {asset_name} is unavailable. Skipping.")
            continue

        current_price = stock_data[4]  # Assuming the 5th column is the price
        purchase_price = current_price  # For now, assume purchase price is the same as current price

        # Calculate profit/loss
        profit_loss = quantity * (current_price - purchase_price)
        net_profit_loss += profit_loss
        total_assets += 1

        # Print the details for this asset
        print(f"{asset_name:<15}{quantity:<10}{purchase_price:<15.2f}{current_price:<15.2f}{profit_loss:<15.2f}")

    print("-" * 70)
    print(f"Total number of assets: {total_assets}")
    print(f"Net Profit/Loss: {net_profit_loss:.2f}\n")

    cursor.close()
    connection.close()

def temporary_portfolio_risk():
    global temp_portfolio

    if not temp_portfolio:
        print("The temporary portfolio is empty. Please add assets to analyze risk.")
        return

    connection, cursor = connect_to_database("Market")
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_date= '2024-04-24'
    init_date= None

    val=0
    wt=[]
    returns = []

    print("Calculating risk assessment for the temporary portfolio...\n")

    for asset in temp_portfolio:
        asset_name = asset['asset_name']
        quantity = asset['quantity']

        # Fetch historical prices from the Market database
        query = f"SELECT date, price FROM Stocks WHERE name='{asset_name}' and date='{current_date}'"
        cursor.execute(query)
        curr_prices = cursor.fetchone()

        print(curr_prices)

        arr=[]
        temp=(quantity*curr_prices)
        val+=temp
        wt.append(temp)        

        one_year_ago = current_date - relativedelta(years=1)
        init_date = one_year_ago.strftime("%Y-%m-%d")
        # query2 = f"SELECT * FROM STOCKS WHERE date = '{init_date}' and Name={row[2]}"
        query2 = f"SELECT * FROM STOCKS WHERE Name='{asset}' and date = '{init_date}'"
        print(query2)
        cursor.execute(query2)
        result2 = cursor.fetchone()
        arr.append(result2[4])

        time.sleep(2)

        six_month_ago = current_date - relativedelta(months=6)
        init_date = six_month_ago.strftime("%Y-%m-%d")
        # query2 = f"SELECT * FROM STOCKS WHERE date = '{init_date}' and Name={row[2]}"
        query2 = f"SELECT * FROM STOCKS WHERE Name='{asset}' and date = '{init_date}'"

        print(query2)
        cursor.execute(query2)
        result2 = cursor.fetchone()
        arr.append(result2[4])

        time.sleep(2)

        one_month_ago = current_date - relativedelta(months=1)
        init_date = one_month_ago.strftime("%Y-%m-%d")
        # query2 = f"SELECT * FROM STOCKS WHERE date = '{init_date}' and Name={row[2]}"
        query2 = f"SELECT * FROM STOCKS WHERE Name='{asset}' and date = '{init_date}'"

        print(query2)
        cursor.execute(query2)
        result2 = cursor.fetchone()
        arr.append(result2[4])

        time.sleep(2)

        init_date = current_date.strftime("%Y-%m-%d")
        # query2 = f"SELECT * FROM STOCKS WHERE date = '{init_date}' and Name={row[2]}"
        query2 = f"SELECT * FROM STOCKS WHERE Name='{asset}' and date = '{init_date}'"

        print(query2)
        cursor.execute(query2)
        result2 = cursor.fetchone()
        arr.append(result2[4])

    for i in range(len(wt)):
        wt[i]=wt[i]/val
    # Example asset returns and weights
    weights = np.array(wt)  # Portfolio weights of 3 assets
    returns = np.array(arr)

    print(weights)
    print(returns)

    # Calculate covariance matrix
    cov_matrix = np.cov(returns)

    # Portfolio variance
    portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))

    # Portfolio standard deviation (risk)
    portfolio_risk = np.sqrt(portfolio_variance)

    print(f'Portfolio Risk (Standard Deviation): {portfolio_risk:.4f}')


    cursor.close()
    connection.close()

import plotly.graph_objects as go

def search_asset():
    connection, cursor = connect_to_database("Market")

    # Fetch all asset names from the database
    query = f"SELECT DISTINCT Name FROM Stocks"
    cursor.execute(query)
    result = cursor.fetchall()
    company_list = [row[0] for row in result]

    # Prompt user to enter the asset name
    print("Enter asset name to search:")
    user_input = input()

    # Get top 5 closest matches
    top_matches = get_top_5_closest_matches(user_input, company_list)

    connection, cursor = connect_to_database("USERS")

    # Display top matches
    print("Top 5 closest matches:")
    for i, (company, score) in enumerate(top_matches, 1):
        print(f"{i}. {company}")

    print(f"{len(top_matches) + 1}. None")
    print("Confirm the company (by entering the number):")
    choice = int(input())

    if choice < 1 or choice > len(top_matches) + 1:
        print("Invalid choice.")
        return

    # If user selects "None", exit
    if choice == len(top_matches) + 1:
        print("No asset selected.")
        return

    confirmed_asset = top_matches[choice - 1][0]

    query = (f"INSERT INTO SEARCH (user_id, query, company, date) "
            f"VALUES ('{user_id}', '{company}', '{top_matches[choice-1][0]}', '{current_date}');")
    
    cursor.execute(query)

    connection.commit()
    print(f"Asset '{confirmed_asset}' selected.")

    # Fetch price data for the last year
    # current_date = datetime.now().strftime("%Y-%m-%d")
    current_date= '2024-04-24'
    # one_year_ago = current_date - relativedelta(years=1)
    one_year_ago= '2023-04-24'

    query_prices = (f"SELECT date, price FROM Stocks "
                    f"WHERE name='{confirmed_asset}' AND date BETWEEN '{one_year_ago}' AND '{current_date}' "
                    f"ORDER BY date")
    cursor.execute(query_prices)
    price_data = cursor.fetchall()



    if not price_data:
        print(f"No price data available for the past year for {confirmed_asset}.")
        return

    # Extract dates and prices for plotting
    dates = [row[0] for row in price_data]
    prices = [row[1] for row in price_data]

    # Plot line chart using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=prices, mode='lines', name=confirmed_asset))
    fig.update_layout(title=f"Price Trend for {confirmed_asset} (Last 1 Year)",
                      xaxis_title="Date",
                      yaxis_title="Price",
                      template="plotly_dark")
    fig.show()

    cursor.close()
    connection.close()



def get_popular_stocks():
    try:
        # Connect to the database
        connection, cursor = connect_to_database("Users")  # Assuming "Users" contains the "Search" table

        # Get the current date and calculate the date 15 days ago
        # current_date = datetime.now().strftime('%Y-%m-%d')
        current_date= '2024-04-24'
        # fifteen_days_ago = (datetime.now() - relativedelta(days=15)).strftime('%Y-%m-%d')
        fifteen_days_ago= '2024-04-05'
        # Query to get popular stocks of the last 15 days
        query = ("""
            SELECT company, COUNT(*) AS search_count
            FROM Search
            WHERE date BETWEEN %s AND %s
            GROUP BY company
            ORDER BY search_count DESC
            LIMIT 10
        """)
        cursor.execute(query, (fifteen_days_ago, current_date))

        # Fetch results
        popular_stocks = cursor.fetchall()

        # Display popular stocks
        print(f"{'Rank':<5}{'Asset Name':<20}")
        print("-" * 20)
        for rank, (stock, count) in enumerate(popular_stocks, start=1):
            print(f"{rank:<5}{stock:<20}{count:<15}")

        # Close connection
        cursor.close()
        connection.close()

        return popular_stocks
    except mysql.connector.Error as err:
        print(f"Error fetching popular stocks: {err}")
        return None

import random
def register_User():
    try:
        # Connect to the USERS database
        connection, cursor = connect_to_database("USERS")

        print("Enter your username: ")
        user=input()
        # Tedra

        print("Enter your password: ")
        # aA4(_Lf>c8@JS4K
        passw=input()

        print("Enter your Mobile Number: ")
        num=int(input())

        print("Enter your Email_id: ")
        email=input()

        print("Please enter your address information")

        print("Enter country: ")
        country=input()

        print("Enter city: ")
        city=input()

        # Generate a unique customer_id
        while True:
            customer_id = random.randint(100000, 999999)  # Generate a 6-digit random ID
            query_check_id = "SELECT * FROM customers WHERE customer_id = %s"
            cursor.execute(query_check_id, (customer_id,))
            if not cursor.fetchone():
                break  # Exit loop if the ID is unique

        # Insert new user into the database
        query_insert = """
            INSERT INTO customers (customer_id, customer_username, customer_password, customer_number, customer_email_ID, customer_city, customer_country)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert, (customer_id, user, passw,num, email, city, country))
        connection.commit()

        print(f"Registration successful! Your Customer ID is: {customer_id}")

        # Close the connection
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error during user registration: {err}")

def sell_asset_from_portfolio(user_id):
    connection, cursor = connect_to_database("PORTFOLIOS")
    if cursor is None:
        print("Failed to connect to the database. Please check your database settings.")
        return

    try:
        # Fetch the user's portfolio ID
        query_portfolio = f"SELECT portfolio_id FROM PORTFOLIO WHERE user_id = '{user_id}'"
        cursor.execute(query_portfolio)
        portfolio_data = cursor.fetchone()
        if not portfolio_data:
            print(f"No portfolio found for user ID: {user_id}")
            return

        portfolio_id = portfolio_data[0]

        # Fetch distinct assets for the user
        query_assets = f"SELECT DISTINCT asset_name, asset_type FROM asset WHERE portfolio_id = '{portfolio_id}'"
        cursor.execute(query_assets)
        assets = cursor.fetchall()

        if not assets:
            print("No assets found in your portfolio.")
            return

        # Display assets with indexing
        print("Your assets:")
        for i, (asset_name, asset_type) in enumerate(assets, start=1):
            print(f"{i}. {asset_name} ({asset_type})")

        # User selects the asset to sell
        choice = int(input("Enter the number corresponding to the asset you want to sell: "))
        if choice < 1 or choice > len(assets):
            print("Invalid choice.")
            return

        selected_asset_name, selected_asset_type = assets[choice - 1]

        # Ask for the quantity to sell
        quantity_to_sell = int(input(f"Enter the quantity of {selected_asset_name} to sell: "))

        # Check total available quantity
        query_quantity = f"SELECT SUM(quantity) FROM asset WHERE portfolio_id = '{portfolio_id}' AND asset_name = '{selected_asset_name}'"
        cursor.execute(query_quantity)
        total_quantity = cursor.fetchone()[0]

        if total_quantity < quantity_to_sell:
            print(f"Insufficient quantity. Available quantity: {total_quantity}")
            return

        # Sell the assets
        remaining_quantity = quantity_to_sell

        while remaining_quantity>0:
            query= f"SELECT asset_id, quantity FROM asset WHERE portfolio_id = '{portfolio_id}' AND asset_name = '{selected_asset_name}' ORDER BY purchase_price ASC LIMIT 1;"
            cursor.execute(query)
            print(query)
            row_quantity = cursor.fetchone()[1]


            if row_quantity <= remaining_quantity:
                # Delete the row if the quantity is less than or equal to the quantity to sell
                query_delete = f"DELETE a FROM asset a JOIN ( SELECT asset_id FROM asset WHERE portfolio_id = '{portfolio_id}' AND asset_name = '{selected_asset_name}' ORDER BY purchase_price ASC LIMIT 1 ) subquery ON a.asset_id = subquery.asset_id;"
                cursor.execute(query_delete)
                remaining_quantity -= row_quantity
            else:
                # Update the row with the reduced quantity
                new_quantity = row_quantity - remaining_quantity
                query_update = f"UPDATE asset a JOIN ( SELECT asset_id FROM asset WHERE portfolio_id = '{portfolio_id}' AND asset_name = '{selected_asset_name}' ORDER BY purchase_price ASC LIMIT 1) subquery ON a.asset_id = subquery.asset_id SET a.quantity = {new_quantity};"
                cursor.execute(query_update)
                remaining_quantity = 0

        connection.commit()
        print(f"Successfully sold {quantity_to_sell} units of {selected_asset_name}.")
    except mysql.connector.Error as err:
        print(f"Error during asset selling: {err}")
    except ValueError:
        print("Invalid input. Please enter numeric values.")
    finally:
        cursor.close()
        connection.close()



# print("Please enter your username: ")
# user=str(input())
# Tedra
# print(getCustomerID(user))
# query1(int(getCustomerID(user)))
# query5()
# query7(getCustomerID(user))
# query3(int(getCustomerID(user)))
# query2(int(getCustomerID(user)))

# connection, cursor = connect_to_database("PORTFOLIOS")

# # user= int(user)
# # print(result)
# query = f"SELECT * FROM Asset "
# # print(query)
# cursor.execute(query)

# result = cursor.fetchall()
# print(result)


# Example usage of new features (can be connected to the menu logic)
# buy_asset()
# portfolio_analysis()
# temporary_portfolio_risk()

# print(temp_portfolio)
# sell_asset("AAPL", 6)
# print(temp_portfolio)
# create_portfolio(getCustomerID(user))

# connection, cursor = connect_to_database("Market")
# query = f"SELECT * FROM Stocks"
# # print(query)
# cursor.execute(query)

# result = cursor.fetchall()
# print(result)

connection, cursor = connect_to_database("Portfolios")
query = f"Delete FROM Asset where asset_name='AAPL'"
# print(query)
cursor.execute(query)
query = f"Delete FROM Asset where asset_name='example_asset_2'"
# print(query)
cursor.execute(query)
connection.commit()

print("--------------------------------------------------Hello!! Welcome to Portfolio Manager-----------------------------------------------------")

cont="y"
while(cont=="y"):
    print("Are you a new User?(y/n)")
    new = input()
    if new == ("y" or "Y"):
        register_User()

    print("Login")
    print("Please enter your username: ")
    user=input()
    # Tedra

    print("Please enter your password: ")
    # aA4(_Lf>c8@JS4K
    passw=input()
    logged_in=False
    
    while(True):

        logged_in=login(user, passw)  
        if logged_in:
            break
        else:
            "Exiting application"
            break
    while logged_in:
        user_id= getCustomerID(user)
        menu()
        print("Chosse any one query: ")
        ch=int(input())
        if(ch==1):
            query1(user_id)
        elif(ch==2):
            sell_asset()
        elif(ch==3):
            buy_asset(user_id)
        elif(ch==4):
            create_portfolio(user_id)
        elif(ch==5):
            query5()
        elif(ch==6):
            search_asset()
        elif(ch==7):
            query7(user_id)
        elif(ch==8):
            get_popular_stocks()
        elif(ch==9):
            cont="n"
            logged_in= False
        else:
            print("Wrong choice!!!")

    else:
        print("Try again")

# sell_asset_from_portfolio(getCustomerID("Tedra"))
