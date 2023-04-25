import pandas as pd
import time
import pyodbc
from sqlalchemy import create_engine, text, Table, Column, Integer, String, MetaData, bindparam


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

# Check if the table already exists, and append data to it if it does
metadata = MetaData()
metadata.reflect(bind=engine)
if table_name in metadata.tables:
    table = Table(table_name, metadata, autoload=True)
    import_order = table.columns.keys()
else:
    import_order = data_df.columns

    # Create table in database
    table = Table(table_name, metadata, Column('id', Integer, primary_key=True, autoincrement=True))
    for col in data_df.columns:
        table.append_column(Column(col, eval(data_types[col])))
    table.create(engine)


# Loop over rows in dataframe and insert into database
rows = []
for row in data_df.itertuples(index=False):
    row_dict = dict(row._asdict())
    row_tuple = tuple(row_dict.values())
    rows.append(row_tuple)
    
    # Prepare the insert query with bind parameters
    insert_query = f"INSERT INTO {table_name} ({', '.join(row_dict.keys())}) VALUES ({', '.join([':' + str(key) for key in row_dict.keys()])})"
    query = text(insert_query).bindparams(*[bindparam(key, value) for key, value in row_dict.items()])
    
   # Check if the row already exists in the database
    select_query = f"SELECT * FROM {table_name}{create_where_clause(row_dict)}"
    result = cnxn.execute(select_query).fetchone()

    # If the row exists, compare the differences and print them
    if result:
        result_dict = dict(zip(row_dict.keys(), result[1:])) # Exclude the 'id' column from the comparison
        differences = [f"{key}: (database) {result_dict[key]} != (CSV) {row_dict[key]}" for key in row_dict if result_dict[key] != row_dict[key]]
        if differences:
            print(f"Row already exists in the database, but there are differences:")
            print("\n".join(differences))
            confirm_overwrite = input("Do you want to overwrite the row? (y/n): ")
            if confirm_overwrite.lower() == 'y':
                # Overwrite the row by updating the existing row
                set_clause = ", ".join([f"{key} = :{key}" for key in row_dict.keys()])
                update_query = f"UPDATE {table_name} SET {set_clause}{create_where_clause(row_dict)}"
                cnxn.execute(text(update_query).bindparams(*[bindparam(key, value) for key, value in row_dict.items()]))
        else:
            print("Row already exists in the database with the same values.")
    else:
        print(f"{', '.join(str(val) for val in row_tuple)}")
        confirm_import = input("Do you want to import this row? (y/n): ")
        if confirm_import.lower() == 'y':
            cnxn.execute(query)
    time.sleep(0.5)


# Commit changes to database and close connection
try:
    print("Committing changes to the database...")
    cnxn.commit()
    print('Data successfully loaded into database!')
except Exception as e:
    print(f"An error occurred while trying to commit changes: {e}")
finally:
    print("Closing the database connection...")
    cnxn.close()
    print("Database connection closed.")
