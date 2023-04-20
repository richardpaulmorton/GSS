import pandas as pd
import time
import pyodbc
from sqlalchemy import create_engine, text, Table, Column, Integer, String


def get_data_types(data_df):
    """Determine data types for each column in dataframe."""
    data_types = {}
    for col, dtype in data_df.dtypes.items():
        if dtype == "object":
            data_types[col] = "VARCHAR(255)"
        elif dtype == "int64":
            data_types[col] = "INT"
        elif dtype == "float64":
            data_types[col] = "FLOAT"
    return data_types

# Replace the following variables with your own database connection details
server = 'localhost'
database = 'GSSdb'
username = 'Python'
password = 'CarmackAttackPython89'

# Create a connection string for the database
connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC Driver 17 for SQL Server'

# Prompt user for table name and file directory
table_name = input('Enter the name of the new table: ')
file_dir = input('Enter the directory of the file to import: ')

# Load data from csv
data_df = pd.read_csv(file_dir)

# Print data types of each column before determining data types
for col in data_df.columns:
    print(f"{col}: {data_df[col].dtype}")

# Determine data types for columns
data_types = get_data_types(data_df)

# Display column names, first row of data, and calculated data types
print(f"The following {len(data_df.columns)} columns were found in the CSV file:")
for col in data_df.columns:
    print(col)
    print(data_df[col][0])
    print(data_types[col])

# Prompt user to confirm or change data types
while True:
    confirm_data_types = input("Do you want to use these data types? (y/n): ")
    if confirm_data_types.lower() == 'y':
        break
    elif confirm_data_types.lower() == 'n':
        # Prompt user to enter new data types
        print("Please enter the data types for each column, separated by commas.")
        print("For example: VARCHAR(255),INT,FLOAT")
        data_type_input = input("Data types: ").split(",")
        for i, col in enumerate(data_df.columns):
            data_types[col] = data_type_input[i]

# Open database connection and create cursor
engine = create_engine(connection_string)
cnxn = engine.connect()

# Create table in database
create_table_query = f"CREATE TABLE {table_name} (id INT IDENTITY(1,1) PRIMARY KEY"
for col in data_df.columns:
    create_table_query += f", {col} {data_types[col]}"
create_table_query += ")"
cnxn.execute(text(create_table_query))

import_order = data_df.columns.tolist()

# Loop over rows in dataframe and insert into database
rows = []
for i, row in enumerate(rows):
    row_tuple = tuple(row)
    insert_query = f"INSERT INTO {table_name} ({', '.join(data_df.columns)}) VALUES ({', '.join(['?' for i in range(len(data_df.columns))])})"
    print(f"Row {i + 1}: {', '.join(str(val) for val in row_tuple)}")
    confirm_import = input("Do you want to import this row? (y/n): ")
    if confirm_import.lower() == 'y':
        cnxn.execute(insert_query, row_tuple)
    time.sleep(0.5)



# Commit changes to database and close connection
cnxn.commit()
cnxn.close()

print('Data successfully loaded into database!')