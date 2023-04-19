from sqlalchemy import create_engine, text

# Replace the following variables with your own database connection details
server = 'localhost'
database = 'GSSdb'
username = 'Python'
password = 'CarmackAttackPython89'

# Create a connection string for the database
connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC Driver 17 for SQL Server'

# Create an engine object to connect to the database
engine = create_engine(connection_string)

# Create a connection object from the engine
conn = engine.connect()

# Test the connection by executing a simple query
query = text('SELECT * FROM dbo.Occupants')
result = conn.execute(query)

# Loop through the result set and print each row
for row in result:
    print(row)

# Close the connection
conn.close()