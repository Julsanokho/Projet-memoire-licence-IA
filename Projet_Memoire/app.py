from flask import Flask, request, render_template
import pickle
import pandas as pd

from flask import Flask, render_template, request, redirect, url_for, session

from flask_mysqldb import MySQL

import MySQLdb.cursors

import re


app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'

app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = 'snkh@19'

app.config['MYSQL_DB'] = 'flask'
mysql = MySQL(app)

model = pickle.load(open("Diabetes.pkl", "rb"))


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():

    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']

        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM accounts WHERE username =%s AND password =%s', (username, password,))

        account = cursor.fetchone()

        if account:
            session['loggedin'] = True

            session['id'] = account['id']

            session['lastname'] = account['lastname']

            msg = 'Logged in successfully !'

            return render_template('home.html', msg=msg)

        else:
            msg = 'Incorrect username / password !'

    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)

    session.pop('id', None)

    session.pop('lastname', None)

    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg =''
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'email' in request.form and 'username' in request.form and 'password' in request.form:

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM accounts WHERE username =%s OR email =%s', (username, email, ))

        account = cursor.fetchone()

        if account:
            msg = 'Account already exists !'

        elif not re.match(r'[A-Za-z]+', firstname):
            msg = 'Invalid firstname !'

        elif not re.match(r'[A-Za-z]+', lastname):
            msg = 'Invalid lastname !'

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'

        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'

        elif not firstname or not lastname or not email or not username or not password:
            msg = 'Please fill out the form !'

        else:
            cursor.execute('INSERT INTO flask.accounts(firstname,lastname,email,username,password) VALUES(%s,%s,%s,%s,%s)', (firstname, lastname, email, username, password))

            mysql.connection.commit()
            msg = 'You have successfully registered !'

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/index')
def prediction():
    return render_template("prediction.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/annuaire')
def annuaire():
    return render_template("annuaire.html")


@app.route('/dicomedical')
def dicimedical():
    return render_template("dicomedical.html")

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    text1 = request.form['1']
    text2 = request.form['2']
    text3 = request.form['3']
    text4 = request.form['4']
    text5 = request.form['5']
    text6 = request.form['6']
    text7 = request.form['7']
    text8 = request.form['8']
    text9 = request.form['9']
    text10 = request.form['10']
    text11 = request.form['11']
    text12 = request.form['12']
    text13 = request.form['13']
    text14 = request.form['14']
    text15 = request.form['15']
    text16 = request.form['16']

    row_df = pd.DataFrame([pd.Series([text1, text2, text3, text4, text5, text6, text7, text8, text9, text10, text11, text12, text13, text14, text15, text16])])
    print(row_df)
    predictions = model.predict_proba(row_df)
    output = '{0:.{1}f}'.format(predictions[0][1], 2)
    output = str(float(output)*100)+'%'
    if output > str(0.5):
        return render_template('result.html', pred=f" Votre probabilité d'avoir le diabète est {output}")
    else:
        return render_template('result.html', pred=f"Felichitation vous ne risquer rien votre probabilité d'avoir le diabète est {output}")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
