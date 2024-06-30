import sqlite3
# def checkaut(username,password):
con = sqlite3.connect('sql.db')
con.execute("CREATE TABLE IF NOT EXISTS DEPARTMENT(ID INTEGER PRIMARY KEY ,NAME VARCHAR(50) NOT NULL UNIQUE)")
con.execute("CREATE TABLE IF NOT EXISTS MYDATA(ID INTEGER PRIMARY KEY AUTOINCREMENT,USERNAME VARCHAR(50) NOT NULL UNIQUE,PASSWORD VARCHAR(255) NOT NULL)")
con.execute('CREATE TABLE IF NOT EXISTS EMPLOYEE(EMPID INTEGER PRIMARY KEY AUTOINCREMENT,DEPARMENTID int REFERENCES DEPARTMENT(id),NAME VARCHAR(50) NOT NULL,SALARY INTEGER NOT NULL)')
con.execute("INSERT INTO EMPLOYEE (DEPARMENTID,NAME,SALARY) VALUES (?, ?, ?)", (1,'robin','500000'))
con.execute("INSERT INTO MYDATA (USERNAME,PASSWORD) VALUES (?, ?)", ('robin','407'))
con.execute("INSERT INTO DEPARTMENT (ID,NAME) VALUES (?, ?)", (1,'MECH'))
con.commit()
    #    result=check.fetchone()
    #    if result:
    #           print(result[0])
    #           if result[0]==password:
    #                     print("password is correct")
    #           else:
    #                     print("user name is not correct")

# checkaut('sooraj','123')