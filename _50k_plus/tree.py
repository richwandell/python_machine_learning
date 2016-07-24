import collections, math
import json, sys


def dumper(obj):
    return obj.__dict__


class Tree:
    
    def __init__(self):
        self.prob = {}
        self.totals = collections.defaultdict(lambda: 0)

    def addSample(self, data, cat): 
        if cat not in self.prob:
            self.prob[cat] = {}  
        self.totals[cat] += 1

        last = []
        for var in data:
            var = var.lower()
            last.append(var)
            index = False
            for l in last:
                if index is False:
                    index = self.prob[cat]
                else:
                    if l not in index:
                        index[l] = {'count': 1}
                    index[l]['count'] += 1
                    index = index[l]
                                    
    def predict(self, data):

        p = {}
        for key in self.prob.keys():
            p[key] = 0

        index1 = False
        index2 = False
        try:
            for key in data:
                key = key.lower()
                if not index1:
                    index1 = self.prob[self.prob.keys()[0]]
                    index2 = self.prob[self.prob.keys()[1]]
                else:
                    if key not in index1:
                        p[self.prob.keys()[1]] += index2['count']
                        break
                    elif key not in index2:
                        p[self.prob.keys()[0]] += index1['count']
                        break

                    index1 = index1[key]
                    index2 = index2[key]
                    p[self.prob.keys()[0]] += index1['count']
                    p[self.prob.keys()[1]] += index2['count']
        except:
            pass

        if p[self.prob.keys()[0]] > p[self.prob.keys()[1]]:
            return self.prob.keys()[0]
        else:
            return self.prob.keys()[1]
    

if __name__ == "__main__":
    
    import pprint, sqlite3
    pp = pprint.PrettyPrinter(indent=4).pprint
     
    db = sqlite3.connect('adult.data.db3')
    cursor = db.cursor()

    columns = """
    workclass, education, marital_status, occupation,
    relationship, race, sex,
    native_country,
    relation_to_50k_plus"""
    
    data = cursor.execute("select %s from adult_data " % columns)
    
    n = Tree()
    for d in data:
        n.addSample(d[:len(d)-1], d[-1])
    open("out.json", "w").writelines(json.dumps(n, default=dumper, indent=2))
    
    data = cursor.execute("select %s from adult_test " % columns)
    
    total = 0
    error = 0
    success = 0
    for d in data:
        total += 1
        prediction = n.predict(d[:-1])
        if prediction != d[-1]:
            error += 1
        else:
            success += 1
        print d[-1], prediction, "Error rate: " + str(100*(float(error)/float(float(error) + float(success))))[:5] + "%"
    print "Total: " + str(total) + " Errors: " + str(error), " Success: " + str(success)
        
        
    print "Stephs Prediction:"
    steph = [
        'Private', 'Bachelors', 'Married-civ-spouse',
        'Prof-specialty', 'Wife', 'White', 'Female', 'United-States', '<=50K'
    ]
    prediction = n.predict(steph[:-1])

    print prediction, steph[-1]

    print "Rich's Prediction:"
    rich = [
        'Private', 'Bachelors', 'Married-civ-spouse',
        'Prof-specialty', 'Husband', 'White', 'Male', 'United-States', '>50K'
    ]

    prediction = n.predict(rich[:-1])

    print prediction, rich[-1]