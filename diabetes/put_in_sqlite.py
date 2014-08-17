import sqlite3, pprint
pp = pprint.PrettyPrinter(indent=4).pprint

db = sqlite3.connect('diabetic_data.db3')

cursor = db.cursor()

file = open("diabetic_data.csv", "r").readlines()
columns = [word for word in file[0].split(",")]
cursor.execute("drop table if exists diabetic_data;")
cursor.execute("""
create table diabetic_data (
    encounter_id integer, patient_nbr integer, race text, gender text,
    age text, weight text, admission_type_id integer, discharge_disposition_id integer,
    admission_source_id integer, time_in_hospital integer, payer_code text, 
    medical_specialty text, num_lab_procedures integer, num_procedures integer,
    num_medications integer, number_outpatient integer, number_emergency integer,
    number_inpatient integer, diag_1 text, diag_2 text, diag_3 text,
    number_diagnoses integer, max_glu_serum text, A1Cresult text, metformin text,
    repaglinide text, nateglinide text, chlorpropamide text, glimepiride text,
    acetohexamide text, glipizide text, glyburide text, tolbutamide text,
    pioglitazone text, rosiglitazone text, acarbose text, miglitol text,
    troglitazone text, tolazamide text, examide text, citoglipton text,
    insulin text, `glyburide-metformin` text, `glipizide-metformin` text, 
    `glimepiride-pioglitazone` text, `metformin-rosiglitazone` text, `metformin-pioglitazone` text,
    change text, diabetesMed text, readmitted text
);
""")

for row in file[1:]:
    cursor.execute("insert into diabetic_data values ('"+"','".join(row.replace('\n', "").split(","))+"');")
    

db.commit()




