import sqlite3
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify, make_response
import numpy as np
import pickle
import sklearn
import pandas as pd
import snowflake.connector

app = Flask(__name__)
app.config["DEBUG"] = True

# Snowflake connection parameters
account = 'ckb61329.prod3.us-west-2.aws'
user = 'trentbuckholz'
password = 'Roshi321!'
warehouse = 'compute_wh'
database = 'TUVA_PROJECT_DEMO'
schema = 'TUVA_SYNTHETIC'
table = 'MEDICAL_CLAIM'

# Establish a connection to Snowflake
conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    warehouse=warehouse,
    database=database,
    schema=schema
)

# Create a cursor to execute SQL queries
cur = conn.cursor()
# Query the Snowflake dataset
query = f"SELECT * FROM {table}"
cur.execute(query)
# Retrieve the data
data = cur.fetchall()
# Close the cursor and connection
cur.close()
conn.close()
# Process and use the data in your frontend application
# Example: Display the data
for row in data:
    print(row)


# conn = sqlite3.connect('database.db')
# print ("Opened database successfully")
# #use SQLite implicit rowid primary key instead of creating our own
# # TODO: Change line below to create our db schemas when we decide upon one.
# #conn.execute('CREATE TABLE IF NOT EXISTS isastudent2 (firstname TEXT, lastname TEXT, tuition TEXT, dipged TEXT, college TEXT, major TEXT, degree TEXT, verification INTEGER, package INTEGER, gender TEXT, momed TEXT, daded TEXT, sibs TEXT, family16 TEXT, parusa TEXT, granusa TEXT, pol TEXT, msg TXT)')
# print ("Table created successfully")
# conn.close()


# @app.route("/", methods = ['GET'])
# def hello():
#   print("Handling request to home page.")
#   # TODO: update this to route to our home page
#   return render_template('')


if __name__ == "__main__":
    app.run(debug=True)