import sqlite3

conn = sqlite3.connect("residence.db")
curs = conn.cursor()
curs.execute("CREATE TABLE Student ("     \
             "StuID char(9) PRIMARY KEY," \
             "NetID varchar(25),"         \
             "FName varchar(25),"         \
             "LName varchar(25),"         \
             "PName varchar(50),"         \
             "Phone char(10),"            \
             "PassHash char(40)"          \
             ")")

curs.execute("CREATE TABLE Contract ("    \
             "StuID char(9) PRIMARY KEY," \
             "Bldg varchar(25),"          \
             "Room varchar(4),"           \
             "Bdrm char(1),"              \
             "Pet int"                    \
             ")")

curs.execute("CREATE TABLE CheckIn ("     \
             "StuID char(9) PRIMARY KEY," \
             "Pname varchar(25),"         \
             "Phone char(10),"            \
             "Sig varchar(50),"           \
             "Date text"                  \
             ")")

curs.execute("INSERT INTO Student VALUES (\"123456789\", \"tmctesterson\", \"Testy\", \"McTesterson\", \"Testy McTesterson\", \"0123456789\", \"14c6eff06744e696cd986f6d5ba8324585f06ab8\")")
curs.execute("INSERT INTO Contract VALUES (\"123456789\", \"Geoffroy\", \"4025\", \"B\", 1)")
conn.commit()
