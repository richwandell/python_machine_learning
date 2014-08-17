import numpy as np
import sklearn,sqlite3,pprint
from sklearn.linear_model import SGDClassifier

pp = pprint.PrettyPrinter(indent=4).pprint
db = sqlite3.connect('adult.data.db3')
cursor = db.cursor()

columns = """
age, workclass, education, education_num, marital_status, occupation, 
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

data = cursor.execute("select %s from adult_data" % columns).fetchall()
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
for row in cursor.execute("select %s from adult_test" % columns).fetchall():    
    xd, yd = createNPRow(row)    
    check = clf.predict(xd)[0]
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
    24, 'Private', 'Bachelors', 13, 'Married-civ-spouse', 
    'Prof-specialty', 'Wife', 'White', 'Female', 'United-States', '<=50K'
]
xd, yd = createNPRow(steph)
check = clf.predict(xd)[0]
prediction = possibilities['relation_to_50k_plus'][check]
actual = possibilities['relation_to_50k_plus'][yd]
print prediction, actual
print "Rich's Prediction:"
rich = [
    32, 'Private', 'Bachelors', 13, 'Married-civ-spouse', 
    'Prof-specialty', 'Husband', 'White', 'Male', 'United-States', '>50K'
]
xd, yd = createNPRow(rich)
check = clf.predict(xd)[0]
prediction = possibilities['relation_to_50k_plus'][check]
actual = possibilities['relation_to_50k_plus'][yd]
print prediction, actual
