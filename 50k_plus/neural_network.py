import numpy as np
import sklearn,sqlite3,pprint
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import *
from pybrain.supervised.trainers import RPropMinusTrainer

pp = pprint.PrettyPrinter(indent=4).pprint
db = sqlite3.connect('adult.data.db3')
cursor = db.cursor()

columns = """
workclass, education, marital_status, occupation,
relationship, race, sex,
native_country,
relation_to_50k_plus"""

cursor.execute("select %s from adult_data limit 1" % columns)

names = list(map(lambda x: x[0], cursor.description))
possibilities = {}
for name in names:
    data = cursor.execute("SELECT distinct %s from adult_data" % name)
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
                print column, "not an int or long"         
    return np.array(nr[:-1]), nr[-1]

data = cursor.execute("select %s from adult_data" % columns).fetchall()

dataset = SupervisedDataSet(8, 1)
for row in data:
    xd, yd = createNPRow(row)       
    dataset.addSample(xd, yd)

nn = buildNetwork(8, 3, 1)
trainer = RPropMinusTrainer(nn)
trainer.setData(dataset)

for x in range(5):
    error = trainer.train()
    print error
  
errors, success = 0,0
for row in cursor.execute("select %s from adult_test" % columns).fetchall():    
    xd, yd = createNPRow(row)    
    check = int(round(nn.activate(xd[:8])[0]))
    if check > 1: check = 1
    prediction = possibilities['relation_to_50k_plus'][check]
    actual = possibilities['relation_to_50k_plus'][yd]
    if prediction == actual:
        match = "match"
        success += 1
    else:
        match = "no match"
        errors += 1
    print prediction, actual, match, errors, success, "Error rate: "+str(100*float(float(errors) / float(errors + success)))[:5]+'%'
   
print "Stephs Prediction:"
steph = [
    'Private', 'Bachelors', 'Married-civ-spouse',
    'Prof-specialty', 'Wife', 'White', 'Female', 'United-States', '<=50K'
]
xd, yd = createNPRow(steph)
check = int(round(nn.activate(xd[:10])[0]))    
if check > 1: check = 1
prediction = possibilities['relation_to_50k_plus'][check]
actual = possibilities['relation_to_50k_plus'][yd]
print prediction, actual
print "Rich's Prediction:"
rich = [
    'Private', 'Bachelors', 'Married-civ-spouse',
    'Prof-specialty', 'Husband', 'White', 'Male', 'United-States', '>50K'
]
xd, yd = createNPRow(rich)
check = int(round(nn.activate(xd[:10])[0]))    
if check > 1: check = 1
prediction = possibilities['relation_to_50k_plus'][check]
actual = possibilities['relation_to_50k_plus'][yd]
print prediction, actual
