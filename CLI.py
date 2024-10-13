import subprocess
from collections import Counter
import re
from datetime import datetime, timedelta
import mysql.connector
# import matplotlib.pyplot as plt
import pandas as pd

print("--------------------------------------------------Hello!! Welcome to Portfolio Manager-----------------------------------------------------")
def menu():
    print("1. Get analysis of your portfolio")
    print("2. Sell assets")
    print("3. Buy assets")
    print("4. Get analysis of similar assets")
    print("5. Get top 10 assets of each category")
    print("6. Portfolio Comparison")
    print("7. Risk Assesment of Portfolio")
    print("8. Show all users")
    print("9. Exit")

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
    
# Create View Books(ISBN, Title, Pub-Year, Availability, Price, BookStore) AS
# SELECT ISBN, Title, Pub-Year, Availability, Unit_Price AS Price, 'BookStore1' AS Bookstore
# FROM BookStore1
# WHERE Availability = 'Yes' and [Title =? OR Unit_Price [</>/<=/>=/=]];
# UNION
# SELECT ISBN, BTitle AS Title, Year-of-Publication AS Pub-Year, Inventory AS Availability, Price,
# 'BookStore2'
# AS Bookstore
# FROM BookStore2
# WHERE Availability = 'Yes' and [Title =? OR ISBN=?OR Unit_Price [</>/<=/>=/=]];
# UNION
# SELECT ISBN, Book_Title AS Title, Publication-Year AS Pub-Year, InStock AS Availability,
# Price, 'BookStore3'
# AS Bookstore
# FROM BookStore3
# WHERE Availability = 'Yes' and [Title =? OR ISBN=?OR Unit_Price [</>/<=/>=/=]];



def create_sql_view(cursor, view_name, query):
    """Creates a view in MySQL."""
    try:
        cursor.execute(f"CREATE OR REPLACE VIEW {view_name} AS {query}")
        print(f"View '{view_name}' created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to fetch data from the view
def fetch_view_data(cursor, view_name):
    """Fetches data from the created view and stores it in a Pandas DataFrame."""
    query = f"SELECT * FROM {view_name}"
    cursor.execute(query)
    
    # Fetch all the rows
    rows = cursor.fetchall()
    
    # Get column names
    column_names = [i[0] for i in cursor.description]
    
    # Store data in a Pandas DataFrame
    data_frame = pd.DataFrame(rows, columns=column_names)
    return data_frame
    
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

cont="y"
while(cont=="y"):
    type=0
    print("Please enter your username: ")
    user=input()

    print("Please enter your password: ")
    passw=input()
    logged_in=False
    # while(type!=1 or type!=2):
    #     print("Are you a:")
    #     print("1. Customer")
    #     print("2. Admin")
    #     # print("3. Exit")
    #     type= int(input())

        # if(type==1):
        #     logged_in=login(user, passw ,"customer")
        # elif(type==2):
        #     logged_in=login(user, passw ,"admin")
        # if logged_in:
        #     break
        # elif(type==3 or logged_in==False):
        #     "Exiting application"
        #     break
    # if logged_in:
    #     menu()
    #     print("Chosse any one query: ")
    #     ch=int(input())
        # if(ch==1):
        #     query1()
        # elif(ch==2):
        #     query2()
        # elif(ch==3):
        #     query3()
        # elif(ch==4):
        #     query4()
        # elif(ch==5):
        #     # Fetch total duration for each platform
        #     total_durations = fetch_total_duration()

        #     # Convert duration to seconds
        #     total_durations_seconds = [(platform[0], timedelta(hours=platform[1].seconds // 3600, minutes=(platform[1].seconds // 60) % 60, seconds=platform[1].seconds % 60)) for platform in total_durations]

        #     # Plotting
        #     labels = [platform[0] for platform in total_durations_seconds]
        #     durations_seconds = [duration[1].total_seconds() for duration in total_durations_seconds]

        #     plt.pie(durations_seconds, labels=labels, autopct='%1.1f%%', startangle=90)
        #     plt.title('Total Duration Distribution by Platform')
        #     plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        #     plt.show()
        # elif(ch==6):
        #     print("Hang on while updating your data...")
        #     subprocess.run(["/home/arbiter/Desktop/IIA/venv/bin/python", "/home/arbiter/Desktop/IIA/schedulerCode.py"])
        # elif(ch==7):
        #     query7()
        # elif(ch==8):
        #     query8()
        # elif(ch==9):
        #     cont="n"
        # else:
        #     print("Wrong choice!!!")

    # else:
    #     print("Try again")

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