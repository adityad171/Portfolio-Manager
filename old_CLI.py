import subprocess
from collections import Counter
import re
from datetime import datetime
import mysql.connector
from dateutil.relativedelta import relativedelta
import pandas as pd
import time
import numpy as np

print("--------------------------------------------------Hello!! Welcome to Portfolio Manager-----------------------------------------------------")
def menu():
    print("1. Get analysis of your portfolio")
    print("2. Sell assets")
    print("3. Buy assets")
    # print("4. Get analysis of similar assets")
    print("5. Get top 10 assets")
    print("7. Risk Assesment of Portfolio")
    print("8. Exit")

def choose_duration():
    print("1. 1 day")
    print("2. 1 month")
    print("3. 1 year")

def login(username, password, type):

    connection, cursor = connect_to_database("USERS")
    if connection is None:
        print("Could not connect to the database.")
        return False
    
    # cursor = connection.cursor()

    # SQL query to find the customer
    query = f"SELECT * FROM {type}s WHERE {type}_username = %s AND {type}_password = %s"
    # print(query)
    cursor.execute(query, (username, password))
    
    # Fetch one result
    result = cursor.fetchone()
    # print(result)

    # Close the connection
    cursor.close()
    connection.close()

    if result:
        print("Customer found.")
        return True
    else:
        print("Customer not found.")
        return False
    
    
def connect_to_database(database_name):
    connection = mysql.connector.connect(
        host='localhost',  # Replace with your MySQL host
        user='root',  # Replace with your MySQL username
        password='@Aditya171',  # Replace with your MySQL password
        database=database_name
    )
    cursor = connection.cursor()
    return connection, cursor




connection = mysql.connector.connect(
        host='localhost',  # Replace with your MySQL host
        user='root',  # Replace with your MySQL username
        password='@Aditya171',  # Replace with your MySQL password
    )
cursor = connection.cursor()


def getCustomerID(username):
    connection, cursor = connect_to_database("USERS")
    if connection is None:
        print("Could not connect to the database.")
        return False
    
    # SQL query to find the customer
    query = f"SELECT * FROM customers WHERE customer_username = '{username}'"
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
    # print(result)

    # print(result)
    query = f"SELECT * FROM Asset WHERE portfolio_id = '{result}'"
    
    print(query)
    cursor.execute(query)

    result = cursor.fetchall()
    # print(result)

    assets=0
    net=0
    # avg=0
    # temp=0

    for row in result:
        print(row)
        assets+=1
        net+=(row[4]*(row[6]-row[5]))
    # Close the connection
    # cursor.close()
    # connection.close()
    print(f"number of assets: {assets}")
    print(f"Net Profit/loss: {net}")

# def query2(user):
#     # Connect to the PORTFOLIOS database
#     connection2, cursor2 = connect_to_database("PORTFOLIOS")
    
#     user = int(user)

#     # Fetch the user's portfolio
#     query = f"SELECT * FROM PORTFOLIO WHERE user_id = '{user}'"
#     cursor2.execute(query)
#     result2 = cursor2.fetchone()[0]
    
#     # Get the list of stocks the user owns
#     query = f"SELECT asset_name, quantity, current_price FROM asset WHERE portfolio_id = '{result2}'"
#     cursor2.execute(query)
#     owned= cursor2.fetchall()
#     dict_owned={}
#     list_owned=[]
#     for row in owned:
#         a=0
#         if row[0] in dict_owned:
#             a = dict_owned.get(row[0])
#         dict_owned.update({row[0]: a+row[1]})

#     if not owned:
#         print("You do not own any stocks.")
#         return

#     print("Your stocks:")
#     i=1
#     for stock in dict_owned:
#         list_owned.append(stock)
#         print(f"{i}. Stock: {stock}, Quantity: {dict_owned.get(stock)}")
#         i+=1
    
#     print("Enter the stock name you want to sell:")
#     stock_to_sell = int(input())
    
#     print("Enter the quantity to sell:")
#     quantity_to_sell = int(input())

#     if quantity_to_sell > dict_owned.get(list_owned[stock_to_sell-1]):
#         print(f"Insufficient quantity. You only own {dict_owned.get(list_owned[stock_to_sell-1])} shares.")
#         return

#     # Connect to the Market database to get the current stock price
#     connection, cursor = connect_to_database("Market")
#     current_date = datetime.now()
#     date_formated = current_date.strftime("%Y-%m-%d")

#     query = f"SELECT * FROM Stocks WHERE name='{list_owned[stock_to_sell-1]}'"
#     cursor.execute(query)
#     result = cursor.fetchone()

#     if not result:
#         print("Stock data not found for today.")
#         return

#     current_price = result[4]
#     print(f"Selling price for {stock_to_sell}: {current_price}")

    # Calculate remaining quantity after sale
    # remaining_quantity = dict_owned.get(list_owned[stock_to_sell-1]) - quantity_to_sell

    # query = f"SELECT * FROM Asset WHERE name='{list_owned[stock_to_sell-1]} AND portfolio_id = '{result2}'"
    # cursor2.execute(query)
    # result2 = cursor2.fetchall()

    # for row in result2:
    #     curr_quantity= row[4]
    #     quantity_to_sell-=curr_quantity
    #     if quantity_to_sell > 0:
    #         query = f"UPDATE asset SET quantity = '{quantity_to_sell}', current_price = '{current_price}' WHERE asset_name = '{list_owned[stock_to_sell-1]}' AND portfolio_id = '{result2}'"
    #     else:
    #         query = f"DELETE FROM asset WHERE asset_name = '{list_owned[stock_to_sell-1]}' AND portfolio_id = '{result2}'"
        
    # try:
    #     # If quantity remains, update the asset. If sold out, remove the asset from the portfolio.
    #     while remaining_quantity > 0:
    #         query = f"UPDATE asset SET quantity = '{remaining_quantity}', current_price = '{current_price}' WHERE asset_name = '{list_owned[stock_to_sell-1]}' AND portfolio_id = '{result2}'"
    #         if remaining_quantity<=0:
    #             query = f"DELETE FROM asset WHERE asset_name = '{list_owned[stock_to_sell-1]}' AND portfolio_id = '{result2}'"
        
    #     cursor2.execute(query)
    #     connection2.commit()
    #     print("Stock sold successfully.")
    # except Exception as e:
    #     print(f"Error selling stock: {e}")
    # finally:
    #     # Close connections and cursors
    #     cursor.close()
    #     connection.close()
    #     cursor2.close()
    #     connection2.close()


def query3(user):
    # Connect to the Market database
    connection, cursor = connect_to_database("Market")
    query = f"SELECT DISTINCT Name FROM Stocks"
    cursor.execute(query)

    result = cursor.fetchall()
    company_list = [row[0] for row in result]  # List comprehension for cleaner code
    company = chooseCompany(company_list)

    print("Enter quantity:")
    quantity = int(input())

    current_date = datetime.now()
    date_formated = current_date.strftime("%Y-%m-%d")

    # Fetch stock details
    query = f"SELECT * FROM Stocks WHERE name='{company}' AND date='{date_formated}'"
    print(query)
    cursor.execute(query)
    result = cursor.fetchone()
    print(result)

    # Sleep to avoid overwhelming the database
    time.sleep(3)

    # Connect to the PORTFOLIOS database
    connection2, cursor2 = connect_to_database("PORTFOLIOS")
    user = int(user)

    # Fetch the user's portfolio
    query = f"SELECT * FROM PORTFOLIO WHERE user_id = '{user}'"
    cursor2.execute(query)
    result2 = cursor2.fetchone()[0]

    # Insert new asset into the 'asset' table
    query = (f"INSERT INTO asset (asset_id, portfolio_id, asset_name, asset_type, quantity, purchase_price, current_price) "
             f"VALUES ('{result[0]}', '{result2}', '{result[2]}', 'stock', '{quantity}', '{result[4]}', '{result[4]}');")
    print(query)

    try:
        cursor2.execute(query)
        connection2.commit()  # Commit the transaction to ensure the data is inserted
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        # Close cursors and connections
        cursor.close()
        connection.close()
        cursor2.close()
        connection2.close()
    

def query5():
    choose_duration()
    dur = int(input())
    connection, cursor = connect_to_database("MARKET")
    # connection, cursor2 = connect_to_database("MARKET")

    init_date= None

    current_date = datetime.now()
    date_formated = current_date.strftime("%Y-%m-%d")

    if dur==1:
        one_day_ago = current_date - relativedelta(days=1)
        init_date = one_day_ago.strftime("%Y-%m-%d")
    elif dur==2:
        one_month_ago = current_date - relativedelta(months=1)
        init_date = one_month_ago.strftime("%Y-%m-%d")
    elif dur==3:
        one_year_ago = current_date - relativedelta(years=1)
        init_date = one_year_ago.strftime("%Y-%m-%d")


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
    connection2, cursor2 = connect_to_database("MARKET")

    for row in result:

        arr=[]
        print(row)
        temp=(row[4]*row[6])
        val+=temp
        wt.append(temp)

        one_year_ago = current_date - relativedelta(years=1)
        init_date = one_year_ago.strftime("%Y-%m-%d")
        # query2 = f"SELECT * FROM STOCKS WHERE date = '{init_date}' and Name={row[2]}"
        query2 = f"SELECT * FROM STOCKS WHERE Name='{row[2]}' and date = '{init_date}'"
        print(query2)
        cursor2.execute(query2)
        result2 = cursor2.fetchone()
        arr.append(result2[4])

        time.sleep(2)

        six_month_ago = current_date - relativedelta(months=6)
        init_date = six_month_ago.strftime("%Y-%m-%d")
        # query2 = f"SELECT * FROM STOCKS WHERE date = '{init_date}' and Name={row[2]}"
        query2 = f"SELECT * FROM STOCKS WHERE Name='{row[2]}' and date = '{init_date}'"

        print(query2)
        cursor2.execute(query2)
        result2 = cursor2.fetchone()
        arr.append(result2[4])

        time.sleep(2)

        one_month_ago = current_date - relativedelta(months=1)
        init_date = one_month_ago.strftime("%Y-%m-%d")
        # query2 = f"SELECT * FROM STOCKS WHERE date = '{init_date}' and Name={row[2]}"
        query2 = f"SELECT * FROM STOCKS WHERE Name='{row[2]}' and date = '{init_date}'"

        print(query2)
        cursor2.execute(query2)
        result2 = cursor2.fetchone()
        arr.append(result2[4])

        time.sleep(2)

        init_date = current_date.strftime("%Y-%m-%d")
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


import jellyfish

# Function to calculate Jaro-Winkler similarity and return top 5 closest matches
def get_top_5_closest_matches(user_input, company_list):
    # List to store company names and their similarity scores
    similarity_scores = []
    
    # Calculate Jaro-Winkler similarity between the input and each company name in the list
    for company in company_list:
        score = jellyfish.jaro_winkler_similarity(user_input, company)
        similarity_scores.append((company, score))
    
    # Sort the companies based on similarity score in descending order
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Get top 5 closest matches
    top_5_matches = similarity_scores[:5]
    
    return top_5_matches

# Example usage
# List of company names in the database
# company_list = [
#     "Microsoft Corporation",
#     "Apple Inc.",
#     "Google LLC",
#     "Amazon.com, Inc.",
#     "Meta Platforms, Inc.",
#     "Tesla, Inc.",
#     "Alphabet Inc.",
#     "Netflix, Inc.",
#     "Uber Technologies, Inc.",
#     "Zoom Video Communications, Inc."
# ]

# User input company name
# user_input = "Apple"
def chooseCompany(company_list):
    print("Enter company Name: ")
    company= input()
    # Get top 5 closest matches
    top_matches = get_top_5_closest_matches(company, company_list)

    # Print the top 5 matches with their similarity scores
    print("Top 5 closest matches:")
    i=1
    for company, score in top_matches:
        print(company)
        print(score)
        if(score>0.5):
            print(f"{i}. {company}")
        i+=1
    print("Confirm the company (by entering the number):")
    confirm= int(input())
    return top_matches[confirm-1][0]

    

# chooseCompany(company_list)

print("Please enter your username: ")
user=str(input())
# Tedra
# print(getCustomerID(user))
# query1(int(getCustomerID(user)))
# query5()
# query7(getCustomerID(user))

connection, cursor = connect_to_database("Market")
query = f"SELECT * FROM Stocks"
# print(query)
cursor.execute(query)

result = cursor.fetchall()
print(result)

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



cont="y"
while(cont=="y"):
    print("Please enter your username: ")
    user=input()

    print("Please enter your password: ")
    passw=input()
    logged_in=False
    
    while(True):

        logged_in=login(user, passw)  
        if logged_in:
            break
        else:
            "Exiting application"
            break
    if logged_in:
        getCustomerID(user)
        menu()
        print("Chosse any one query: ")
        ch=int(input())
        if(ch==1):
            query1()
        elif(ch==2):
            
        elif(ch==3):
            query3()
        elif(ch==4):
            query4()
        elif(ch==5):
            # Fetch total duration for each platform
            total_durations = fetch_total_duration()

            # Convert duration to seconds
            total_durations_seconds = [(platform[0], timedelta(hours=platform[1].seconds // 3600, minutes=(platform[1].seconds // 60) % 60, seconds=platform[1].seconds % 60)) for platform in total_durations]

            # Plotting
            labels = [platform[0] for platform in total_durations_seconds]
            durations_seconds = [duration[1].total_seconds() for duration in total_durations_seconds]

            plt.pie(durations_seconds, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.title('Total Duration Distribution by Platform')
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            plt.show()
        elif(ch==6):
            print("Hang on while updating your data...")
            subprocess.run(["/home/arbiter/Desktop/IIA/venv/bin/python", "/home/arbiter/Desktop/IIA/schedulerCode.py"])
        elif(ch==7):
            query7()
        elif(ch==8):
            query8()
        elif(ch==9):
            cont="n"
        else:
            print("Wrong choice!!!")

    else:
        print("Try again")

    create_sql_view(cursor, "General_view", """SELECT 
    U.customer_id,
    U.customer_username,
    P.portfolio_id,
    P.user_id,
    R.report_id,
    R.portfolio_id
FROM 
    USERS.Customers U
JOIN 
    PORTFOLIOS.Asset P ON U.customer_id = P.user_id
JOIN 
    REPORTS.Performance R ON P.portfolio_id = R.portfolio_id;""")

    print(fetch_view_data(cursor, "General_view"))

    cursor.close()
    connection.close()