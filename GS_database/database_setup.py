from faker import Faker
import pyodbc
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://user:password@localhost/GSS_DB?driver=ODBC Driver 17 for SQL Server'

# Connect to MS SQL Server using Windows Authentication
server = 'NOVUS'
database = 'GSSdb'
username = 'Python'
password = 'CarmackAttackPython89'
driver = '{ODBC Driver 17 for SQL Server}'
# Create the SQLAlchemy database URI for SQL Server
db_uri = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'

# Configure Flask to use SQLAlchemy with the URI for SQL Server
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy instance
db = SQLAlchemy(app)

# Define your database models as usual using the db instance
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

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

# Example route that uses the database
@app.route('/')
def hello_world():
    # Query the User table and return the usernames
    users = User.query.all()
    usernames = [user.username for user in users]
    return f'Hello, {", ".join(usernames)}!'
