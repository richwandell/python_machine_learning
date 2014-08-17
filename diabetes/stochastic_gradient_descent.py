import numpy as np
import sklearn,sqlite3,pprint
from sklearn.linear_model import SGDClassifier

pp = pprint.PrettyPrinter(indent=4).pprint
db = sqlite3.connect('diabetic_data.db3')
cursor = db.cursor()

columns = """
race, gender, age, weight, admission_type_id,
discharge_disposition_id, admission_source_id,
time_in_hospital, medical_specialty,
num_lab_procedures, num_procedures, num_medications,
number_outpatient, number_emergency, number_inpatient, 
diag_1, diag_2, diag_3, number_diagnoses, max_glu_serum,
A1Cresult, metformin, repaglinide, nateglinide, chlorpropamide, 
glimepiride, acetohexamide, glipizide, glyburide, tolbutamide, 
pioglitazone, rosiglitazone, acarbose, miglitol, troglitazone, 
tolazamide, examide, citoglipton, insulin, `glyburide-metformin`,
`glipizide-metformin`, `glimepiride-pioglitazone`, `metformin-rosiglitazone`,
`metformin-pioglitazone`, change, diabetesMed, readmitted
"""

cursor.execute("select %s from diabetic_data limit 1" % columns)

names = list(map(lambda x: x[0], cursor.description))
possibilities = {}
for name in names:
    data = cursor.execute("SELECT distinct `%s` from diabetic_data" % name)
    possibilities[name] = [d[0] for d in data.fetchall()]
    
def createNPRow(row):
    nr = []
    for i, column in enumerate(row):
        try:
            num = possibilities[names[i]].index(column)
            nr.append(num)
        except:
            if isinstance(column, (int, long)):
                num = min(possibilities[names[i]], key=lambda x:abs(x-column))
                nr.append(num)    
                print num, column   
            else:
                print column, "not an int or long"         
    return np.array(nr[:-1]), nr[-1]

data = cursor.execute("select %s from diabetic_data limit 100000" % columns)
X, y = [],[]
for row in data:
    xd, yd = createNPRow(row)       
    X.append(xd)
    y.append(yd)
    
X = np.array(X)
y = np.array(y)
 
clf = SGDClassifier(loss="hinge", penalty="l2")
clf.fit(X, y)
  
errors, success = 0,0
for row in cursor.execute("select %s from diabetic_data limit 100000, 101766" % columns).fetchall():    
    xd, yd = createNPRow(row)    
    check = clf.predict(xd)[0]
    prediction = possibilities['readmitted'][check]
    actual = possibilities['readmitted'][yd]
    if prediction == actual:
        match = "match"
        success += 1
    else:
        match = "no match" 
        errors += 1
    print prediction, actual, match, errors, success, "Error rate: "+str(100*float(float(errors) / float(errors + success)))[:5]+'%'

