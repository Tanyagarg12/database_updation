import pyodbc
from tabulate import tabulate
import csv

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-V2FT1Q6;"  
    "DATABASE=testdb;"         
    "UID=DESKTOP-V2FT1Q6\\manoj;" 
    "PWD=admin;"   
    "Trusted_Connection=yes;"   
)

# Connect to the database
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Execute the query
query = """
SELECT 
    Page AS [Page], 
    LineItem AS [Line Item], 
    FieldName AS [Field Name], 
    LineNumber AS [Line Number], 
    StopColumn AS [Stop Column],
    Size as [Size]
FROM dbo.tblcd121Reference ORDER BY Page ASC;
"""
cursor.execute(query)

# Fetch all rows
rows = cursor.fetchall()

# Print the results in tabular format
headers = ["Page", "Line Item", "Field Name", "Line Number", "Stop Column", "Size"]
print(tabulate(rows, headers=headers, tablefmt="grid"))

# Save the results to a CSV file
with open("output.csv", "w", newline="", encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(headers) 
    for row in rows:
        csvwriter.writerow(row)  

# Close the cursor and connection
cursor.close()
conn.close()


