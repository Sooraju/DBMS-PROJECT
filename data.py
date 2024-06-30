import sqlite3
from flask import Flask,request,redirect,url_for,render_template

app=Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return checkaut(username, password)  # Return the result of checkaut
    else:
        return render_template('login.html') 

@app.route('/add',methods=['GET','POST'])
def add():
     if request.method =='POST':
          id=request.form['id']
          name=request.form['name']
          print(f"Received id: {id}, name: {name}")  # For debugging
          outcom=inputdepartment(id,name)
     return render_template('add_department.html',result=outcom)

      
@app.route('/register',methods=['POST'])
def welcome():
    username = request.form['username']
    password = request.form['password']
    print(f"Received username: {username}, password: {password}")  # For debugging
    inputregister(username,password)
    return render_template('login.html')


# @app.route('/login/home',methods=['GET','POST'])
# def home():
#     return render_template('login.html')
strid=0
@app.route('/home')
def home():
    return redirect(url_for('login'))


@app.route('/add_department',methods=['POST'])
def add_department():
    return render_template('add_department.html')


@app.route('/storeid',methods=['POST'])
def storeid():
    strid = request.form['id']
    return render_template('updateconferm.html',strid=strid)



@app.route('/updatedata/<int:strid>',methods=['POST','GET'])
def updatedata(strid):
    id = request.form['id']
    DEPT = request.form['DEPT']
    print(f"Received id: {id}, name: {DEPT} strind :{strid}")  # For debugging
    con = sqlite3.connect('sql.db')
    con.execute("UPDATE DEPARTMENT SET ID=?,NAME=? WHERE ID=?", (id, DEPT,strid))
    con.commit()
    con.close()
    return render_template('update_data.html',result="success")


@app.route('/update_data',methods=['POST','GET'])
def update_data():
     return render_template('update_data.html')



@app.route('/add_employee',methods=['POST','GET'])
def add_employee():
     return render_template('add_employee.html') 


@app.route('/add_employee_adddatabase',methods=['POST','GET'])
def add_employee_adddatabase():
    department=request.form['department']
    name=request.form['name']
    salary=request.form['salary']
    print(f"Received department: {department}, name: {name}, salary: {salary}")   
    return addemploye(department,name,salary)



@app.route('/updateemp_data',methods=['POST','GET'])
def updateemp_data():
     return render_template('updateemp_data.html')


@app.route('/storeempname',methods=['POST','GET'])
def storeempname():
     empname=request.form['empname']
     print(f"Received empname: {empname}")
     con=sqlite3.connect('sql.db')
     responce=con.execute("SELECT EMPID FROM EMPLOYEE WHERE LOWER(name) = LOWER(?)", (empname,))
     mydata=responce.fetchone()
     con.close()
     print(mydata)
     if mydata:
          return render_template('updateempconferm.html',empname=empname)
     else:
          return render_template('updateemp_data.html',result='error')


@app.route('/updateempdata/<string:empname>',methods=['POST','GET'])
def updateempdata(empname):
     department=request.form['DEPT']
     empnameup=request.form['name']
     salary=request.form['salary']
     print(f"Received department: {department}, name: {empnameup}, salary: {salary},empname:{empname}")
     return updateempdata(empname,department,empnameup,salary)

@app.route('/deletedepartment_data',methods=['POST','GET'])
def deletedepartment_data():
    return render_template('deletedepartment_data.html')


@app.route('/confermdepartment_delete',methods=['POST','GET'])
def confermdepartment_delete():
     depname=request.form['departmentname']
     con=sqlite3.connect('sql.db')
     res=con.execute("DELETE FROM DEPARTMENT WHERE LOWER(NAME)=LOWER(?)", (depname,))
     print(res)
     con.commit()
     con.close()
     return render_template('deletedepartment_data.html')

@app.route('/deleteemploye_data',methods=['POST','GET'])
def deleteemploye_data():
    return render_template('deleteemploye_data.html')


@app.route('/deleteemployee_conferm',methods=['POST','GET'])
def deleteemployee_conferm():
     depart=request.form['DEPT']
     employeename=request.form['name']
     con=sqlite3.connect('sql.db')
     cursor=con.cursor()
     cursor.execute("SELECT 1 FROM EMPLOYEE WHERE LOWER(name)=LOWER(?)", (employeename,))
     resultname=cursor.fetchone()
     con.close()
     con=sqlite3.connect('sql.db')
     cursor=con.cursor()
     cursor.execute("SELECT 1 FROM DEPARTMENT WHERE LOWER(name)=LOWER(?)", (depart,))
     resultdepart=cursor.fetchone()
     con.close()
     if resultname and resultdepart:
          con=sqlite3.connect('sql.db')
          con.execute('''
                      DELETE FROM EMPLOYEE 
                      WHERE EMPID IN(
                      SELECT EMPID FROM EMPLOYEE
                      WHERE LOWER(NAME)=LOWER(?) AND DEPARMENTID IN(
                      SELECT ID FROM DEPARTMENT
                      WHERE LOWER(NAME)=LOWER(?)
                      )
                      )
                      ''', (employeename, depart))
          con.commit()
          con.close()
          return render_template('deleteemploye_data.html')
     else:
          print(resultname)
          print(resultdepart)
          return render_template('deleteemploye_data.html ')
         

def updateempdata(empname,department,empnameup,salary):
     con = sqlite3.connect('sql.db')
     responc=con.execute("SELECT DEPARMENTID FROM EMPLOYEE WHERE LOWER(name) = LOWER(?)", (empname,))
     mydata=responc.fetchone()
     print(mydata)
     if mydata:
            id=mydata[0]
            print(id)
            con.execute("UPDATE EMPLOYEE SET DEPARMENTID=?,NAME=?,SALARY=? WHERE NAME=?", (department, empnameup,salary,empname))
            con.commit()
            con.close()
            return render_template('updateempconferm.html',result='success')
     else:
          return render_template('updateemp_data.html',result='error')
     

def addemploye(department,name,salary):
     con = sqlite3.connect('sql.db')
     con.execute('CREATE TABLE IF NOT EXISTS EMPLOYEE(EMPID INTEGER PRIMARY KEY AUTOINCREMENT,DEPARMENTID int REFERENCES DEPARTMENT(id),NAME VARCHAR(50) NOT NULL,SALARY INTEGER NOT NULL)')
     responce=con.execute('SELECT ID FROM DEPARTMENT WHERE NAME=?', (department,))
     mydata=responce.fetchone()
     con.commit()
     print(mydata)
     if mydata:
         id=mydata[0]
         print(id)
         con.execute("INSERT INTO EMPLOYEE (DEPARMENTID,NAME,SALARY) VALUES (?, ?, ?)", (id, name, salary))
         con.commit()
         con.close()
         return render_template('add_employee.html',result='success')
     else:
          return render_template('add_employee.html',result='error')



def inputregister(username,password):
        con = sqlite3.connect('sql.db')
        # Insert data into the table
        # con.execute("DROP TABLE MYDATA")
        con.execute("CREATE TABLE IF NOT EXISTS MYDATA(ID INTEGER PRIMARY KEY AUTOINCREMENT,USERNAME VARCHAR(50) NOT NULL UNIQUE,PASSWORD VARCHAR(255) NOT NULL)")
        con.execute("INSERT INTO MYDATA (USERNAME,PASSWORD) VALUES (?, ?)", (username, password))
        con.commit()  # Commit the changes
        res = con.execute("SELECT * FROM mydata")
        mydata = res.fetchall()
        print(mydata)  # This should now work
        con.close()


def inputdepartment(id,name):
     con=sqlite3.connect('sql.db')
     con.execute("CREATE TABLE IF NOT EXISTS DEPARTMENT(ID INTEGER PRIMARY KEY ,NAME VARCHAR(50) NOT NULL UNIQUE)")
     con.execute("INSERT INTO DEPARTMENT (ID,NAME) VALUES (?, ?)", (id, name))
     con.commit()
     res=con.execute("SELECT * FROM DEPARTMENT")
     mydata=res.fetchall()
     print(mydata)
     con.close()
     return "success"


def checkaut(username,password):
       con = sqlite3.connect('sql.db')
       check = con.execute("SELECT PASSWORD FROM MYDATA WHERE USERNAME=?", (username,))
       con.execute("CREATE TABLE IF NOT EXISTS DEPARTMENT(ID INTEGER PRIMARY KEY ,NAME VARCHAR(50) NOT NULL UNIQUE)")
       info=con.execute("SELECT * FROM DEPARTMENT")
       mydata=info.fetchall()
       leng=len(mydata)
       print(leng)
       print(mydata)
       result=check.fetchone()
       info1=con.execute("SELECT E.NAME,E.SALARY,D.NAME FROM EMPLOYEE E JOIN DEPARTMENT D ON E.DEPARMENTID=D.ID")
       mydata1=info1.fetchall()
       leng1=len(mydata1)
       print(mydata1)
       con.close()
       if result:
              print(result[0])
              if result[0]==password:
                    return render_template('introdata.html',info=mydata,lent=leng,info1=mydata1,lent1=leng1)
              else: 
                     print("incorrect password")
                     return render_template('login.html',alert="incorrect password")

       else:
            print("Username not found")
            return render_template('login.html', alert="Username not found.")
       

if __name__=='__main__':
    app.run(debug=True)




# for i in range(len(mydata)):
#            print(mydata[i][1])
# con.close()