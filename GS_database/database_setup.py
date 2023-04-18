from faker import Faker
import pyodbc
import random
import numpy as np

# Connect to MS SQL Server using Windows Authentication
server = 'NOVUS'
database = 'GSSdb'
username = 'Python'
password = 'CarmackAttackPython89'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';TrustServerCertificate=True;PWD=' + password)
# Generate fake data for the Occupants table
fake = Faker()
age_mean = 24
age_stddev = 15  # adjust this value to control the spread of the distribution
ages = np.random.normal(age_mean, age_stddev, 1000)
for i in range(1000):
    first_name = fake.first_name()
    middle_name = fake.first_name()
    last_name = fake.last_name()
    age = int(ages[i])
    gender = fake.random_element(elements=('Male', 'Female'))
    dna_code = fake.uuid4()
    health_status = fake.random_element(elements=('Healthy', 'Sick', 'Critical'))
    location = fake.random_element(elements=('Living Quarters', 'Mess Hall', 'Lab', 'Medical Bay'))

    # Insert record into Occupants table
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO Occupants (FirstName, MiddleName, LastName, Age, Gender, DNACode, HealthStatus, Location) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", first_name, middle_name, last_name, age, gender, dna_code, health_status, location)
    cursor.commit()

# Close the database connection
cnxn.close()
