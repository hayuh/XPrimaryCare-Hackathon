import sqlite3
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify, make_response
import numpy as np
import pickle
import sklearn
import pandas as pd
import snowflake.connector
import gzip
import json

app = Flask(__name__)
app.config["DEBUG"] = True



# Snowflake connection parameters
account = 'ckb61329.prod3.us-west-2.aws'
user = 'trentbuckholz'
password = 'Roshi321!'
warehouse = 'compute_wh'
database = 'TUVA_PROJECT_DEMO'
schema = 'TUVA_SYNTHETIC'

# # Query parameters.
# select_attributes = ''
# for i in range(1, 26):
#     select_attributes += f'm.diagnosis_code_{i}, '
# select_attributes += 'm.paid_amount, p.ndc_code'
# from_tables = 'MEDICAL_CLAIM as m, PHARMACY_CLAIM as p'
# where_conditions = 'diagnosis_code_1 is not null and p.ndc_code is not null and m.patient_id = p.patient_id'

# Establish a connection to Snowflake
conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    warehouse=warehouse,
    database=database,
    schema=schema
)

# # Create a cursor to execute SQL queries
# cur = conn.cursor()
# # Query the Snowflake dataset
# query = f"SELECT {select_attributes} FROM {from_tables} WHERE {where_conditions}"
# cur.execute(query)
# # Retrieve the data
# data = cur.fetchall()
# # Get the column names
# column_names = [desc[0] for desc in cur.description]

# # Close the cursor and connection
# cur.close()
# conn.close()

# Getting all unique values in diagnostic codes
# Create a cursor to execute SQL queries
cur = conn.cursor()
# Query the Snowflake dataset
query = f"select distinct diagnosis_code_1 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_2 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_3 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_4 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_5 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_6 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_7 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_8 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_9 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_10 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_11 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_12 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_13 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_14 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_15 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_16 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_17 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_18 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_19 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_20 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_21 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_22 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_23 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_24 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_25 from tuva_synthetic.medical_claim"
cur.execute(query)
# Retrieve the data
diag_codes_sql = cur.fetchall()
#Convert diagnosis codes into array
diag_codes = pd.DataFrame(diag_codes_sql).to_numpy().flatten()
diag_codes = list(diag_codes)
diag_codes = json.dumps(diag_codes[1:])
# Close the cursor and connection
cur.close()
conn.close()

COLUMNS = ['DIAGNOSIS_CODE_1', 'DIAGNOSIS_CODE_2', 'DIAGNOSIS_CODE_3',
       'DIAGNOSIS_CODE_4', 'DIAGNOSIS_CODE_5', 'DIAGNOSIS_CODE_6',
       'DIAGNOSIS_CODE_7', 'DIAGNOSIS_CODE_8', 'DIAGNOSIS_CODE_9',
       'DIAGNOSIS_CODE_10', 'DIAGNOSIS_CODE_11', 'DIAGNOSIS_CODE_12',
       'DIAGNOSIS_CODE_13', 'DIAGNOSIS_CODE_14', 'DIAGNOSIS_CODE_15',
       'DIAGNOSIS_CODE_16', 'DIAGNOSIS_CODE_17', 'DIAGNOSIS_CODE_18',
       'DIAGNOSIS_CODE_19', 'DIAGNOSIS_CODE_20', 'DIAGNOSIS_CODE_21',
       'DIAGNOSIS_CODE_22', 'DIAGNOSIS_CODE_23', 'DIAGNOSIS_CODE_24',
       'DIAGNOSIS_CODE_25', 'PAID_AMOUNT']

# Getting the model.
with gzip.open('model_pickle.gz', 'rb') as f:
    model = pickle.load(f)

with gzip.open('encoder_pickle.gz', 'rb') as f:
    # Technically this a encoder/decoder since its a bidict
    encoder = pickle.load(f)



# def preprocess(data):
#     for i, row in enumerate(data):
#         row = row[:-2] + (1 if row[-2] > 0 else 0, row[-1])
#         data[i] = row
#     return data


# data = preprocess(data)
# # Process and use the data in your frontend application
# # Convert the data to a DataFrame
# df = pd.DataFrame(data, columns=column_names)
# print(df)


# Honestly this is really ugly but I'm tired. - it works for now.
# Critique: Its 12:16am and I just realized that I'm representing paid_amount
# as 0 or 1 (num representation of boolean) however I also have 0 and 1 mapped
# to strings in the encoder/model...might make a difference might not.
def return_med_prediction(diagnosis_list):
    if len(diagnosis_list) > 25:
        raise ValueError('only 25 conditions are allowed')
    diagnosis_list_final = []
    for i in range(25):
        if i < len(diagnosis_list):
            # Diagnosis needs to be encoded as int since model can only interpret numbers.
            diagnosis_list_final.append(encoder[diagnosis_list[i]])
        else:
            diagnosis_list_final.append(encoder[None])
    diagnosis_list_final.append(1)
    print(diagnosis_list_final)
    return encoder.inverse[model.predict(pd.DataFrame([diagnosis_list_final], columns=COLUMNS))[0]]

#print(return_med_prediction(['M25551', 'M79604']))


# conn = sqlite3.connect('database.db')
# print ("Opened database successfully")
# #use SQLite implicit rowid primary key instead of creating our own
# # TODO: Change line below to create our db schemas when we decide upon one.
# #conn.execute('CREATE TABLE IF NOT EXISTS isastudent2 (firstname TEXT, lastname TEXT, tuition TEXT, dipged TEXT, college TEXT, major TEXT, degree TEXT, verification INTEGER, package INTEGER, gender TEXT, momed TEXT, daded TEXT, sibs TEXT, family16 TEXT, parusa TEXT, granusa TEXT, pol TEXT, msg TXT)')
# print ("Table created successfully")
# conn.close()

@app.route("/", methods = ['GET', 'POST'])
def main_page():
    print("Handling request to home page.")
    if request.method == 'GET':
        return render_template('main.html', diag_codes=diag_codes)
    elif request.method=='POST':
        num_codes = request.form.get('num_codes')
        submitted_diag_codes = []
        for i in range(0, int(num_codes)):
            submitted_diag_codes.append(request.form.get('input-box-' + str(i)))
        print(num_codes)
        print(submitted_diag_codes)
        pred = return_med_prediction(submitted_diag_codes)
        print(pred)
        return render_template('results.html', prediction=pred)

if __name__ == "__main__":
    app.run(debug=True)
