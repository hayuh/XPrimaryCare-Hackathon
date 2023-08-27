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
# account = 'ckb61329.prod3.us-west-2.aws'
# user = 'trentbuckholz'
# password = 'Roshi321!'
# warehouse = 'compute_wh'
# database = 'TUVA_PROJECT_DEMO'
# schema = 'TUVA_SYNTHETIC'

# # Query parameters.
# select_attributes = ''
# for i in range(1, 26):
#     select_attributes += f'm.diagnosis_code_{i}, '
# select_attributes += 'm.paid_amount, p.ndc_code'
# from_tables = 'MEDICAL_CLAIM as m, PHARMACY_CLAIM as p'
# where_conditions = 'diagnosis_code_1 is not null and p.ndc_code is not null and m.patient_id = p.patient_id'

# Establish a connection to Snowflake
# conn = snowflake.connector.connect(
#     user=user,
#     password=password,
#     account=account,
#     warehouse=warehouse,
#     database=database,
#     schema=schema
# )

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
# cur = conn.cursor()
# # Query the Snowflake dataset
# query = f"select distinct diagnosis_code_1 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_2 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_3 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_4 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_5 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_6 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_7 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_8 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_9 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_10 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_11 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_12 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_13 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_14 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_15 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_16 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_17 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_18 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_19 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_20 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_21 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_22 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_23 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_24 from tuva_synthetic.medical_claim UNION ALL select distinct diagnosis_code_25 from tuva_synthetic.medical_claim"
# cur.execute(query)
# # Retrieve the data
# diag_codes_sql = cur.fetchall()
# #Convert diagnosis codes into array
# diag_codes = pd.DataFrame(diag_codes_sql).to_numpy().flatten()
# diag_codes = list(diag_codes)
# diag_codes = json.dumps(diag_codes[1:])
# # Close the cursor and connection
# cur.close()
# conn.close()

diag_codes = ["M25551", "R310", "Z79899", "K5750", "R928", "J441", "Z7901", "I4891", "I509", "Z01812", "J449", "R0600", "R799", "E1122", "I480", "R609", "E785", "E7800", "I2510", "Z981", "J029", "D0359", "I5032", "R9431", "E041", "R404", "F332", "R000", "R0902", "R739", "L603", "M48061", "Z87891", "I214", "H578", "Z043", "J9811", "E038", "M170", "I619", "H43819", "I499", "L309", "Z45010", "K8020", "H2511", "G4733", "R42", "Z79891", "Z6824", "S99919A", "H35373", "J9690", "L578", "I517", "E669", "I6340", "R413", "J209", "J9600", "R110", "M5020", "F3181", "Z9861", "F209", "R197", "E049", "B351", "N390", "C44311", "I10", "H26491", "H35363", "Z1231", "R911", "R0602", "R1011", "N401", "J986", "M1009", "Z0001", "K529", "R0603", "H04123", "I639", "E569", "R1013", "M79672", "E8352", "R21", "R002", "M549", "R4182", "K922", "R55", "Z86010", "Z23", "E119", "R8299", "E875", "E109", "H25043", "R918", "E039", "M179", "M545", "R109", "Z0000", "K2270", "M1611", "I519", "N12", "M1711", "M19072", "N898", 
"M542", "N359", "Z125", "C4441", "Z87440", "M25552", "R0789", "S065X9A", "Q998", "M94261", "L03116", "J9602", "M899", "N3020", "I5189", "J95821", "C44519", "M4802", "E118", "N950", "H40003", "K432", "E782", "H25013", "Z85828", "D519", "Z85038", "F1120", "I6789", "I5033", "R634", "K635", "I493", "L03032", "H43811", "R069", "K4090", "K436", "J45909", "Z4789", "R3129", "G43119", "N951", "Z1211", "Z01811", "F1020", "J40", "F39", "J432", "G459", "L84", "J310", "Z955", "E890", "L570", "S2242XA", "R52", "M5416", "N486", "M2550", "M1712", "Z98890", "I6529", "Z853", "S20219A", "L820", "J342", "Z8546", "J218", "D259", "R1033", "L900", "E8881", "B20", "F319", "I080", "J301", "L718", "H2513", "I951", "B078", "M40205", "I350", "M25562", "M4316", "D485", "R1310", "I4892", "F0390", "E559", "N183", "D649", "T148", "M9901", "R300", "J189", "R7989", "R102", 
"E780", "L308", "M5442", "H353112", "R319", "J302", "K810", "M25561", "B029", "K2900", "M25662", "I5031", "Z950", "Z8719", "R0609", "I255", "R030", "H25811", "I2699", "H3532", "H43813", "N3090", "I495", "M069", "N179", "K429", "E784", "I481", "E1165", "Z452", "H6983", "R410", "M25569", "K621", "H2512", "I340", "I219", "L600", "M47817", "R9720", "G8929", "E1142", "I482", "D472", "I447", "L989", "I309", "M47816", "S098XXA", 
"Z951", "R311", "H25812", "M4727", "C61", "Z4889", "D529", "T1490", "M9981", "I25118", "S0081XA", "I6523", "L720", "D123", "K828", "J690", "S90416A", "Z124", "M5136", "S79912A", "M2041", "I70203", "H2640", "J90", "R7301", "M48062", "Z800", "R339", "E0590", "K219", "R140", "I82A21", "I739", "M25462", "E8342", "Z5309", "E1129", "M7741", "R531", "R221", "R0601", "M5440", "J312", "R152", "M6281", "L242", "Z136", "F29", "S93401A", "M064", "R112", "E063", "S72142A", "M25512", "J069", "H35343", "S93602A", "N184", "J4520", "M23221", "C44329", "S90112A", "R601", "C4361", "Z77090", "D122", "R279", "M19011", "K5909", "D492", "N281", "R8290", "I674", "Z8639", "L821", "L818", "R809", "I63512", "H1850", "G9340", "M79606", "K6389", "I313", "R5381", "C9110", "M47812", "D508", "H40053", "G43709", "R748", "K819", "L814", "R600", "H4011X2", "I341", "J9620", "N1330", "R933", "J849", "R238", "K629", "H33012", "H353113", "M152", "R7309", "H8113", "Z08", "I25110", "R072", "Z510", "S299XXA", "M2042", "M79641", "Z131", "N838", "I130", "E113511", "S9032XA", "L03115", "K589", "F331", "Z9229", "R100", "H401133", "I081", "Z01818", "N939", "R05", "F419", "J4530", "M797", "K5730", "R498", "M1990", "F329", "I638", "M6282", "I440", "Z87898", "I348", "H40023", "S199XXA", "Z130", "R12", "Z09", "M1812", "I200", "M62838", "G43809", "R509", "E1140", "H26492", "Z9911", "N289", "I119", "K2970", "M7662", "Z01419", "C55", "Z6828", "I7300", "M79642", "Z95818", "G360", "Z1159", "L299", "H53453", "M2012", "J9589", "D127", "M79644", "J341", "I70213", "Z5181", "R1032", "K8010", "Z780", "K754", "D500", "I2109", "D235", "D7589", "R262", "M859", "K5660", "M546", "I351", "E871", "R040", "R1084", "H348310", "I63511", "R0989", 
"H52201", "N959", "H8110", "G5603", "J181", "Z4509", "D72829", "G319", "G40909", "H903", "E113393", "D045", "R6889", "H1045", "M79604", "R202", "M75110", "I83893", "D473", "E291", "R808", "Z862", "D229", "D494", "S92355A", "R0981", "J9692", "H4011X1", "H401124", "I5022", "H3531", "K317", "R768", "H26493", "A6920", "Z952", "N761", "I771", "N393", "S42211A", "M1389", "H4311", "I82442", "R740", "H1813", "H16143", "E042", "B070", "H02831", "R6881", "C44219", "N812", "R3914", "A498", "R4781", "M8589", "E1169", "H61032", "R972", "E0789", "H6123", "G510", "F1910", "M5117", "H4011X3", "R944", "A09", "Q619", "N8111", "E860", "K5790", "C679", "K209", "I259", "N3021", "D1801", "S72012A", "J988", "M75120", "D0439", "C44622", "D225", "H353211", "Z9189", "E1121", "T07", "Z8249", "I5023", "M25519", "H5034", "R778", "M3210", "I498", "M25531", "S2241XD", "J4521", "K5732", "I82531", "M5412", "M533", "Z1329", "E7801", "I120", "M7581", "G2111", "L0390", "F0150", "K8050", "M7050", "H401191", "J80", "H401121", "S82402A", "H01003", "M7061", "K869", "R1909", "I4510", "G309", "Z45018", "H401433", "M79602", "H16141", "L300", "N358", "D72828", "H259", "I25708", "D696", "M9904", "M26609", "C801", "H26499", "R948", "M940", "H2000", "N763", "S0003XA", "M25579", "I8311", "H538", "L303", "R0781", "L739", "R938", "K3580", "K6289", "J810", "N8110", "M436", "M7120", "Z791", "N993", "D124", "D1779", "Z5111", "H7291", "L259", "S42212A", "R4702", "M0689", "N644", "K829", "K909", "L851", "N201", "D692", "H4051X3", "E878", "E790", "R1900", "K5100", "H5015", "I82401", "J0380", "G4761", "I7389", "B9681", "C44229", "M4854XA", "E11321", "D699", "D518", "T07XXXA", "J9622", "E113293", "M19049", "B349", "C3490", "F5101", 
"Z13220", "I82409", "M5414", "K7460", "M85852", "R278", "E8351", "M461", "N6011", "I160", "L243", "F328", "C228", "R1111", "I671", "R260", "C44112", "L859", "D400", "H1820", "H401222", "L02611", "L03114", "M47896", "K4191", "M205X2", "F69", "Z96653", "H4312", "M65332", "F3131", "E46", "G589", "R253", "R87610", "N649", "L111", "A528", "H52203", "C678", "J111", "I4430", "J9621", "N6012", "I358", "R001", "R042", "M810", "J309", "R079", "M4120", "C44529", "Z4682", "I471", "N200", "R1314", "K56609", "M25539", "R350", "L02211", "I714", "N3281", "K52832", "I472", "E230", "M4806", "S0101XA", "R922", "N3000", "I209", "I618", "M8588", "K37", "H401111", "I429", "R195", "H40013", "C4911", "N189", "I420", "R1010", "Z01810", "Z139", "M961", "I359", "A419", "D126", "D239", "I25810", "H43393", "M1612", "I060", "S81811A", "L539", "I25119", "J939", "C44319", "K31819", "H02052", "S72111A", "M5116", "R2241", "Z48815", "R946", "G4730", "R2681", "K5000", "I70211", "M791", "I6521", "Z4502", "N400", "C50912", "H269", "H35361", "Z13820", "D120", "G43909", "R9439", "D509", "R51", "S0083XA", "K861", "Z01411", "K921", "E034", "S0990XA", "H353131", "E538", "M9903", "M0579", "H25813", "D539", "K5289", "R1031", "M25461", "R062", "I82403", "I110", "K7689", "M5030", "R252", "N182", "F909", 
"L708", "M109", "R32", "R61", "M19012", "E440", "M7989", "J040", "M5124", "K449", "R29898", "M4807", "K8590", "F71", "S0501XA", "R309", "M629", "L4050", "M869", "N630", "C49A0", "R945", "B182", "I059", "H4423", "M79671", "J383", "J208", "R5382", "Z4659", "N402", "R570", "H401131", "Z96652", "M4726", "D2372", "K1121", "M4302", "K625", "Q898", "J343", "M9923", "H35041", "B001", "C50412", "R7302", "F3189", "R591", "D0512", "R0982", "M5126", "M7552", "M79605", "M79601", "M1289", "J811", "H34832", "E1049", "I129", "L579", "D3610", "F068", "J439", "L723", "M9902", "N419", "R399", "R401", "K289", "L218", "K22710", "K5641", "F4310", "R251", "R071", "E7211", "S93491D", "E8359", "J0190", "J9601", "R6882", "G8194", "S3993XA", "R7303", "N2889", "H833X3", "L602", "E6601", "G3109", "D0372", "M79675", "Q6211", "S22000A", "M5186", "H353231", "M21611", "N952", "K4021", "J157", "N3946", "C50212", "L659", "D075", "R070", "M7060", "N63", "M659", "N760", "N132", "M779", "I161", "D2339", "Q231", "F17290", "M9983", "Q612", "N3001", "D469", "J0100", "R456", "M722", "I7091", "S40012A", "R351", "E213", "Z961", "B079", "H40002", "I213", "C44612", "D6489", "E11311", "L239", "R0689", "K623", "R8279", "H35371", "H401132", "M160", "K319", "F411", "S72309A", "I872", "K760", "K5791", "M2011", "R1012", "S91111A", "K5792", "C4442", "T1490XA", "M353", "H539", "C50511", "H35033", "N840", "M4722", "D72818", "Z471", "Z95810", "N529", "H35013", "N429", "M174", "H353114", "R312", "E113313", "R29818", "B9689", "C50811", "G4719", "H1131", "J329", "C9000", "H838X3", "K2950", "J3089", "E1310", "G2581", "K51919", "G9612", "C4359", "F320", "L03031", "S83231A", "C44712", "M65321", "H33051", "C8519", "I361", "A429", "S52501A", "E8809", "I441", "D0462", "S3992XA", "C44619", "Z0389", "F422", "S63501A", "G250", "I6522", "Z930", "H4010X0", "Q822", "I700", "N209", "G4700", "M7752", "F309", "M159", "G600", "R222", "L2089", "I5021", "A499", "M19041", "M719", "Z201", "R4020", "H3581", "R7981", "T7840XA", "D72819", "K420", "R269", "E0580", "Z6829", "M130", "N039", "S5011XA", "I272", "H401130", "M7021", "E040", "N62", "T50901A", "E210", "J984", "G4089", "I452", "R160", "D62", "L293", "I6782", "M10072", "M5432", "R590", "I629", "C760", "S99921A", "R17", "N210", "D125", "R200", "R58", "M25432", "F4321", "Z86718", "S93422A", "C44629", "B974", "M129", "G8918", "D631", "Z719", "K224", "Q245", "M4602", "H353132", "Z789", "S8990XA", "N269", "R9430", "F4320", "N320", "Z7722", "S62636A", "K210", "S61451A", "T451X5D", "H906", "Z1272", "S93509A", "N815", "J09X2", "D0471", "C569", "H47233", "N9089", "I83813", "F3341", "R1110", "I150", "D2239", "I70212", "K648", "H9190", "M868X7", "L918", "E1065", "M25661", "F200", "R208", "Z5189", "M5127", "Z7689", "R790", "C439", "E259", "J438", "M5106", "C3491", "D693", "I2119", "I890", "K2960", "A048", "E789", "K2901", "C4331", "R935", "M50323", "M180", "E2839", "M50221", "R209", "S61411A", "E099", "R3912", "M316", "H81319", "C50911", "M4696", "Z13228", "H9193", "S42302A", "I071", "S52502A", "R94131", "I9589", "D510", "H6120", "M4326"];

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
        if request.form.get('num_codes') is None:
            return render_template('main.html', diag_codes=diag_codes)
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
