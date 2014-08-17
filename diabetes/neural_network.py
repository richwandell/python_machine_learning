import numpy as np
import sklearn,sqlite3,pprint
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.datasets            import ClassificationDataSet

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
    last = len(row)
    for i, column in enumerate(row):
        try:
            num = possibilities[names[i]].index(column)
            if i == last-1:
                nr.append(num)
            else:
                ratio = float(float(num) / float(len(possibilities[names[i]])))
                nr.append(ratio)
        except:
            if isinstance(column, (int, long)):
                num = min(possibilities[names[i]], key=lambda x:abs(x-column))
                if i == last-1:
                    nr.append(num)
                else:
                    ratio = float(float(num) / float(len(possibilities[names[i]])))
                    nr.append(ratio)    
                print ratio, column   
            else:
                print column, "not an int or long", possibilities[names[i]], names[i]     
    return np.array(nr[:-1]), nr[-1]
 
dataset = ClassificationDataSet(46, 1, class_labels=possibilities['readmitted'])
for row in cursor.execute("select %s from diabetic_data limit 0, 10000" % columns):
    xd, yd = createNPRow(row)       
    dataset.addSample(xd, yd)

nn = buildNetwork(dataset.indim, 20, dataset.outdim, outclass=SoftmaxLayer)
trainer = BackpropTrainer(nn, dataset=dataset, momentum=0.1, verbose=True, weightdecay=0.01)
print possibilities['readmitted']
print dataset.getField('target')
for x in range(10):
    error = trainer.train()
    print error
   
errors, success = 0,0
for row in cursor.execute("select %s from diabetic_data limit 50000, 101766" % columns):    
    xd, yd = createNPRow(row)    
    check = int(round(nn.activate(xd[:46])[0]))    
    if check > 1: check = 1
    prediction = possibilities['readmitted'][check]
    actual = possibilities['readmitted'][yd]
    if prediction == actual:
        match = "match"
        success += 1
    else:
        match = "no match"
        errors += 1
    print prediction, actual, match, errors, success, "Error rate: "+str(100*float(float(errors) / float(errors + success)))[:5]+'%'
     
