import sqlite3, pprint
pp = pprint.PrettyPrinter(indent=4)

db = sqlite3.connect('adult.data.db3')

cursor = db.cursor()

cursor.execute("""
    create table if not exists adult_test (
        id integer primary key,
        age integer,
        workclass text,        
        fnlwgt integer,
        education text,
        education_num integer,
        marital_status text,
        occupation text,
        relationship text,
        race text,
        sex text,
        capital_gain integer,
        capital_loss integer,
        hours_per_week integer,
        native_country text,
        relation_to_50k_plus text
    );
""")

file = [[word.strip() for word in line.split(",")] for line in open("adult.test", "r").readlines()]
pp.pprint(file[0])
for line in file:
    try:
        d = "insert into adult_test values (null,%s,'%s',%s,'%s',%s,'%s','%s','%s','%s','%s',%s,%s,%s,'%s','%s')" % (
            line[0], line[1], line[2], line[3], 
            line[4], line[5], line[6], line[7], 
            line[8], line[9], line[10], line[11],
            line[12], line[13], line[14].replace(".", "")
        )
        cursor.execute(d)
    except:
        pass
db.commit()




