#Sam
# Import the required libraries
import pandas as pd
import sqlite3

# Load customer and order data from CSV files
customers_df = pd.read_csv('customer.csv')
orders_df = pd.read_csv('orders.csv')

# Merge order data with customer data based on the 'CustomerID' column
merged_df = pd.merge(orders_df, customers_df, on='CustomerID', how='inner')

# Calculate the total amount for each order
merged_df['TotalAmount'] = merged_df['Quantity'] * merged_df['Price']

merged_df['Status'] = merged_df['OrderDate'].apply(lambda d: 'New' if d.startswith('2024-10') else 'Old')


high_value_orders = merged_df[merged_df['TotalAmount'] > 4500]


conn = sqlite3.connect('ecommerce.db')

# Create a table to store high-value orders if it does not already exist
create_table_query = '''
CREATE TABLE IF NOT EXISTS HighValueOrders (
    OrderID INTEGER,
    CustomerID INTEGER,
    Name TEXT,
    Email TEXT,
    Product TEXT,
    Quantity INTEGER,
    Price REAL,
    OrderDate TEXT,
    TotalAmount REAL,
    Status TEXT
)
'''
conn.execute(create_table_query)

# Insert the high-value orders into the database table
high_value_orders.to_sql('HighValueOrders', conn, if_exists='replace', index=False)

# Retrieve and print all records from the 'HighValueOrders' table
result = conn.execute('SELECT * FROM HighValueOrders')
for row in result.fetchall():
    print(row)


conn.close()

print("ETL process completed successfully!")
