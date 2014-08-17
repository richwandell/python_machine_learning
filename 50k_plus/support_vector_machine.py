import numpy as np
import sklearn,sqlite3,pprint
from sklearn import svm
from joblib import Parallel, delayed

def createNPRow(row, possibilities, names):
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

def getPossibility(name):  
    db = sqlite3.connect('adult.data.db3')
    cursor = db.cursor()   
    data = cursor.execute("SELECT distinct %s from adult_data" % name)
    return name, [d[0] for d in data.fetchall()]

if __name__ == "__main__":
    
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
    p = Parallel(n_jobs=-1)(delayed(getPossibility)(name) for name in names)
    possibilities = {x: y for x, y in p}    
    data = cursor.execute("select %s from adult_data" % columns).fetchall()    
    d = Parallel(n_jobs=-1)(delayed(createNPRow)(row, possibilities, names) for row in data)
    X, y = zip(*d)
    X, y = np.array(X), np.array(y)
    clf = svm.SVC()     
    clf.fit(X, y)
      
    errors, success = 0,0
    for row in cursor.execute("select %s from adult_test" % columns):    
        xd, yd = createNPRow(row,possibilities, names)    
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
    xd, yd = createNPRow(steph,possibilities, names)
    check = clf.predict(xd)[0]
    prediction = possibilities['relation_to_50k_plus'][check]
    actual = possibilities['relation_to_50k_plus'][yd]
    print prediction, actual
    print "Rich's Prediction:"
    rich = [
        32, 'Private', 'Bachelors', 13, 'Married-civ-spouse', 
        'Prof-specialty', 'Husband', 'White', 'Male', 'United-States', '>50K'
    ]
    xd, yd = createNPRow(rich,possibilities, names)
    check = clf.predict(xd)[0]
    prediction = possibilities['relation_to_50k_plus'][check]
    actual = possibilities['relation_to_50k_plus'][yd]
    print prediction, actual
