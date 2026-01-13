import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('database/test.db')
cursor = conn.cursor()

# Query to fetch all data from the 'users' table (assuming the table name is 'users' based on the CSV example)
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

# Get column names from the cursor description
columns = [desc[0] for desc in cursor.description]

# Write to CSV
with open('users_data4.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow(columns)
    # Write data
    writer.writerows(rows)

# Close the connection
conn.close()