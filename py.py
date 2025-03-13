#Sam 
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import socket
import platform

income_df = pd.read_excel('income.xlsx')
expenses_df = pd.read_csv('expenses.txt', sep=' ')


income_df['Month'] = pd.to_datetime(income_df['Month'].str.strip(), format='%Y-%m-%d', errors='coerce')
expenses_df['Month'] = pd.to_datetime(expenses_df['Month'].str.strip(), format='%Y-%m-%d', errors='coerce')


if income_df['Month'].isna().any():
    print("Warning: Invalid dates found in income data.")
if expenses_df['Month'].isna().any():
    print("Warning: Invalid dates found in expenses data.")


merged_df = pd.merge(income_df, expenses_df, on='Month', how='inner')


merged_df['Savings'] = merged_df['Income'] - merged_df['Expenses']


if merged_df['Income'].sum() <= 0:
    raise ValueError("Total income must be greater than zero.")
if merged_df['Expenses'].sum() > merged_df['Income'].sum():
    raise ValueError("Total expenses cannot exceed total income.")


expense_percentage = merged_df['Expenses'].sum() / merged_df['Income'].sum() * 100
labels = ['Expenses', 'Savings']
sizes = [max(0, expense_percentage), max(0, 100 - expense_percentage)]

def get_machine_ip():
    # Get the hostname
    hostname = socket.gethostname()
    # Get the IP address
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_machine_name():
    # Get the machine name using platform
    machine_name = platform.node()
    return machine_name

if __name__ == "__main__":
    ip = get_machine_ip()
    name = get_machine_name()
    print(f"Machine IP: {ip}")
    print(f"Machine Name: {name}")


conn = sqlite3.connect('finance_data.db')
merged_df.to_sql('FinanceData', conn, if_exists='replace', index=False)
conn.close()


plt.figure(figsize=(12, 6))


plt.subplot(1, 2, 1)
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title(f'Sam Expense vs Savings Distribution\nMachine: {ip}\nIP: {name}', fontsize=10)


#Draw a line chart
plt.subplot(1, 2, 2)
merged_df.sort_values('Month', inplace=True)
merged_df.set_index('Month')['Savings'].plot(kind='line', marker='o', color='green')
plt.title(f'Sam Monthly Savings Trends\nMachine: {ip}\nIP: {name}', fontsize=10)
plt.xlabel('Month')
plt.ylabel('Savings ($)')

plt.tight_layout()
plt.subplots_adjust(top=0.8)
plt.show()

#Execute SQL query
conn = sqlite3.connect('finance_data.db')
cursor = conn.cursor()

query = """
SELECT Month, Income, Expenses, Savings
FROM FinanceData
WHERE Income > 7000 AND Savings > 400
ORDER BY Month ASC
"""

cursor.execute(query)
results = cursor.fetchall()

for row in results:
    print(row)

conn.close()

def get_machine_ip():
    # Get the hostname
    hostname = socket.gethostname()
    # Get the IP address
    ip_address = socket.gethostbyname(hostname)
    return ip_address