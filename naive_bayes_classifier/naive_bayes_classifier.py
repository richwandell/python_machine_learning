import collections, math
class NaiveBayesClassifier:        
    
    def __init__(self):
        self.prob = {}
        self.totals = collections.defaultdict(lambda: 0)
    
    def addSample(self, data, cat): 
        if cat not in self.prob:
            self.prob[cat] = {}  
        self.totals[cat] += 1     
        for var in data:            
            for var1 in data:
                if var1 != var:
                    if var not in self.prob[cat]:
                        self.prob[cat][var] = collections.defaultdict(lambda: 0)
                    self.prob[cat][var][var1] += 1
                                    
    def predict(self, data):
        probs = collections.defaultdict(lambda: 0)
        for x in self.prob.keys():            
            for y in data:
                for z in data:
                    if y != z:
                        try:                        
                            probs[x] += self.prob[x][y][z]
                        except:
                            probs[x] += 0
                        
        for x in probs.keys():
            probs[x] = float(probs[x]) / float(self.totals[x])
        high = ""
        m = 0
        for x in probs.keys():
            if probs[x] > m:
                m = probs[x]
                high = x
        return high
    
    
    
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
    
    data = cursor.execute("select %s from adult_data" % columns)
    
    n = NaiveBayesClassifier()
    for d in data:
        n.addSample(d[:len(d)-1], d[-1])
    n.train()   
    data = cursor.execute("select %s from adult_test" % columns)
    
    total = 0
    error = 0
    for d in data:
        total+=1
        prediction = n.predict(d[:-1])
        if prediction != d[-1]:
            error += 1
        pp([          
           d[-1], 
           prediction, 
           "Error rate: "+str(100*(float(error)/float(total)))
        ])
        

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    