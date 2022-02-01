from flask import Flask,render_template,request
import pyodbc

# set the project root directory as the static folder, you can set others.
#app = Flask(__name__, static_url_path="/static", static_folder='C:\iSmile TEch\covid (1)\covid\static')
app = Flask(__name__)

passcde=0
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/passcode')
def passcode():
    Fname = request.args.get('Fname')
    Lname = request.args.get('Lname')
    Age = request.args.get('Age')
    Country = request.args.get('Country')
    Zip_code = request.args.get('Zip_code')
    print("-------------------------")
    print(Fname)
    print(Lname)
    print(Age)
    print(Country)
    print(Zip_code)

    import pyodbc

    server = 'virutal.database.windows.net' 
    database = 'COVID19-db' 
    username = 'Ismiledb' 
    password = 'Ismile@123' 
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    cursor.execute("INSERT INTO PersonDetails(LastName,FirstName,Age,City) VALUES (?,?,?,?)",(Lname,Fname,Age,Country))
    cnxn.commit()

    cursor.execute("SELECT max(Personid) FROM PersonDetails WHERE LastName=? AND FirstName=? AND Age=? AND City=?",(Lname,Fname,Age,Country))
    row=cursor.fetchone()
    global passcde
    passcde=row[0]
    print(passcde)

    return render_template('passcode.html',passcde=passcde)

@app.route('/inner')
def inner():
    return render_template('inner.html')

@app.route('/results')
def results():


    server = 'virutal.database.windows.net' 
    database = 'COVID19-db' 
    username = 'Ismiledb' 
    password = 'Ismile@123' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    cursor.execute("SELECT TOP 1 * FROM SensorDetails ORDER BY id DESC")
    row=cursor.fetchone()
    print(row[1])

    cursor.execute("SELECT temperature FROM SensorDetails where id="+str(row[1])+"")
    temperature=cursor.fetchone()
    print(temperature[0])

    return render_template('results.html',temperature=temperature[0])
    #return render_template('barcode.html')
    
@app.route('/barcode')
def barcode():
    passcode=passcde
    return render_template('barcode.html',passcode=passcode)

@app.route('/XrayResult')
def XrayResult():
    personid=passcde
    print(passcde)
    server = 'virutal.database.windows.net' 
    database = 'COVID19-db' 
    username = 'Ismiledb' 
    password = 'Ismile@123' 
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    #cursor.execute("SELECT TOP 1 * FROM dbo.XrayDetails where Personid=?,personid")
    query = "SELECT * FROM dbo.XrayDetails where Personid=?"
    cursor.execute(query,(personid,))
    row=cursor.fetchone()
    #print(row)
    print("--------------------------database connectivity-----------")
    #print("fetched data:"+str(row))
    pred_class=row[3]
    pred_value=row[2]
    #print(type(pred_value))
    #print(pred_class)
    text=""
    if pred_class == '0':
        text="Predicted class: Normal, Likelihood:"+str(pred_value) 
        if pred_value < '0.8':
            text+="with the WARNING of low confidence"            
    else:
        text="Predicted class: Pneumonia, Likelihood:"+str(pred_value)
        if pred_value < '0.8':
            text+="WARNING, low confidence" 

    print("text"+text)
    return render_template('xrayResult.html', result=text)

@app.route('/Rating')
def Rating():    
    print("rating url called")
    star = request.args.get('star')
    print("star {}".format(star))
    return "0"

    

if __name__ == "__main__":
    app.run(debug=True)