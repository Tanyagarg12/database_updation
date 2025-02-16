import pyodbc  # Install using: pip install pyodbc
import pandas as pd

# Connect to the database
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-V2FT1Q6;"  
    "DATABASE=testdb;"         
    "Trusted_Connection=yes;"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Read the final output CSV file
csv_file_path = "finalOuput.csv"
df = pd.read_csv(csv_file_path)

# Function to check if a column exists in a table
def column_exists(table_name, column_name):
    column_name = column_name.strip()  # Remove spaces from CSV column name
    query = f"""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = '{table_name.split('.')[-1]}' 
        AND LOWER(COLUMN_NAME) = LOWER('{column_name}');
    """
    cursor.execute(query)
    return cursor.fetchone() is not None  # If result exists, column is valid

# Function to check if a value is a valid number
def is_valid_number(value):
    try:
        float(value)  # Try converting to float
        return True
    except (ValueError, TypeError):
        return False  # Invalid number

# Loop through each row in the CSV file
for index, row in df.iterrows():
    sysid_str = str(row["SYSID"]).strip().upper()  # Ensure SYSID is string and case-insensitive

    # Trim SYSID (Extract first part and middle part)
    parts = sysid_str.split()
    if len(parts) >= 2:  
        extracted_sysid = parts[1]  # Take the middle part (0000)
        extracted_prefix = parts[0]  # Take the first part (5054)
    else:
        extracted_sysid = sysid_str  # Use full SYSID if format doesn't match
        extracted_prefix = "UNKNOWN"  # Default value if format is incorrect

    # Get Field Name and Extracted Value for insertion
    field_name = row["Field Name"].strip()  # Remove any extra spaces
    extracted_value = row["Extracted Value"]  # Value to insert

    # **Skip invalid values**
    if pd.isna(extracted_value) or not is_valid_number(extracted_value):
        print(f"Skipping: Invalid extracted value '{extracted_value}' for column '{field_name}' in {table_name}")
        continue  # Skip to next row

    # **Handle different queries for each table**
    if "SYS" in sysid_str:
        table_name = "dbo.TBLCD121HISTORY"
        where_clause = f"WHERE system = '{extracted_prefix}'"
    else:
        table_name = "dbo.tblCD121Collections"
        where_clause = f"WHERE system = '{extracted_prefix}' AND prin = '{extracted_sysid}'"

    # **Check if the column exists before running the update**
    if column_exists(table_name, field_name):
        update_query = f"""
            UPDATE {table_name} 
            SET [{field_name}] = {extracted_value} 
            {where_clause};
        """
        
        print(f"\nExecuting query:\n{update_query}")  # Debugging print
        cursor.execute(update_query)  # Use parameterized query
    else:
        print(f"Skipping: Column '{field_name}' does not exist in {table_name}")

# Commit changes
conn.commit()

# Close the connection
cursor.close()
conn.close()

print("\nData updated successfully!")

