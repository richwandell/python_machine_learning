import numpy as np
import sklearn,sqlite3,pprint
from sklearn import svm
from joblib import Parallel, delayed

def createNPRowMulti(possibilities, names, data, num):
    if num == 0:
        d = data[:len(data)/2]
    else:
        d = data[len(data)/2:]
    ret = []
    for row in d:
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
        ret.append([np.array(nr[:-1]), nr[-1]])
    return ret

def createNPRowSingle(row):
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
    workclass, education, marital_status, occupation,
    relationship, race, sex,
    native_country,
    relation_to_50k_plus"""
    print "getting pos"
    cursor.execute("select %s from adult_data limit 1" % columns)    
    names = list(map(lambda x: x[0], cursor.description))    
    p = Parallel(n_jobs=-1,backend="threading")(delayed(getPossibility)(name) for name in names)
    possibilities = {x: y for x, y in p}    
    print "got pos getting all data"
    data = cursor.execute("select %s from adult_data" % columns).fetchall()
    print "got data making par"    
    d = Parallel(n_jobs=2)(delayed(createNPRowMulti)(possibilities, names, data, num) for num in range(2))
    d = d[0]+d[1]    
    X, y = zip(*d)
    X, y = np.array(X), np.array(y)
    print "got all data fitting"
    clf = svm.SVC()     
    clf.fit(X, y)
    print "fit"
    errors, success, total = 0, 0, 0
    for row in cursor.execute("select %s from adult_test" % columns):    
        xd, yd = createNPRowSingle(row)    
        check = clf.predict(xd)[0]
        prediction = possibilities['relation_to_50k_plus'][check]
        actual = possibilities['relation_to_50k_plus'][yd]
        if prediction == actual:
            match = "match"
            success += 1
        else:
            match = "no match"
            errors += 1
        total += 1
        print prediction, actual, match, errors, success, "Error rate: "+str(100*float(float(errors) / float(errors + success)))[:5]+'%'
    print "Total: " + str(total) + " Errors: " + str(errors) + " Success: " + str(success)
       
    print "Stephs Prediction:"
    steph = [
        'Private', 'Bachelors', 'Married-civ-spouse',
        'Prof-specialty', 'Wife', 'White', 'Female', 'United-States', '<=50K'
    ]
    xd, yd = createNPRowSingle(steph)
    check = clf.predict(xd)[0]
    prediction = possibilities['relation_to_50k_plus'][check]
    actual = possibilities['relation_to_50k_plus'][yd]
    print prediction, actual
    print "Rich's Prediction:"
    rich = [
        'Private', 'Bachelors', 'Married-civ-spouse',
        'Prof-specialty', 'Husband', 'White', 'Male', 'United-States', '>50K'
    ]
    xd, yd = createNPRowSingle(rich)
    check = clf.predict(xd)[0]
    prediction = possibilities['relation_to_50k_plus'][check]
    actual = possibilities['relation_to_50k_plus'][yd]
    print prediction, actual
