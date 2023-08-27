import json
from typing import Tuple

import pandas as pd
import snowflake.connector

# Snowflake connection parameters
ACCOUNT = 'ckb61329.prod3.us-west-2.aws'
USER = 'trentbuckholz'
PASSWORD = 'Roshi321!'
WAREHOUSE = 'compute_wh'
DATABASE = 'TUVA_PROJECT_DEMO'
SCHEMA = 'TUVA_SYNTHETIC'


def _preprocess(data: Tuple[Tuple[str]]):
    """Preprocesses raw data from snowflake for use in machine learning.

    Updates PAID_AMOUNT column to 0/1 depending on if insurance paid any sum
    of money for a medication.

    Args:
        data: 2D tuple of data retrieved from snowflake query.

    Returns:
        The preprocessed data.
    """
    for i, row in enumerate(data):
        row = row[:-2] + (1 if int(row[-2]) > 0 else 0, row[-1])
        data[i] = row
    return data


def get_claims_data() -> pd.DataFrame:
    """Gets relevant data from snowflake, for use in machine learning.

    Returns:
        Pandas DataFrame of the data ready for use in machine learning.
    """
    # Query parameters.
    select_attributes = ''
    for i in range(1, 26):
        select_attributes += f'm.diagnosis_code_{i}, '
    select_attributes += 'm.paid_amount, p.ndc_code'
    from_tables = 'MEDICAL_CLAIM as m, PHARMACY_CLAIM as p'
    where_conditions = 'diagnosis_code_1 is not null and p.ndc_code is not null and m.patient_id = p.patient_id'

    # Establish a connection to Snowflake
    conn = snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT,
        warehouse=WAREHOUSE,
        database=DATABASE,
        schema=SCHEMA
    )
    # Create a cursor to execute SQL queries
    cur = conn.cursor()
    try:
        # Query the Snowflake dataset
        query = f"SELECT {select_attributes} FROM {from_tables} WHERE {where_conditions}"
        cur.execute(query)
        # Retrieve the data
        data = cur.fetchall()
        # Get the column names
        column_names = [desc[0] for desc in cur.description]
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

    # Process and use the data in your frontend application
    # Convert the data to a DataFrame
    return pd.DataFrame(_preprocess(data), columns=column_names)
