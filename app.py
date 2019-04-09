from flask import Flask,render_template,request,redirect
import Login

app = Flask(__name__)

use = Login

@app.route('/')
def hello_world():
    return render_template('login_grade.html')

@app.route('/login',methods=['post'])
def login():
    a = request.get_data()
    print(a)
    username  = request.form['account']
    password = request.form['password']
    password1 = request.form['password1']
    year = request.form['current_year']
    term = request.form['current_term']
    student = Login.Who(username, password)
    cha = use.University(student, password1)
    cha.login()
    results = cha.GradeTestResults(year,term)
    print(results)
    return render_template('Showgrade.html',results = results,year=year,term=term)


@app.route(('/highest'))
def highest():
    results = use.University.highest_grade()
    return render_template('Showgrade.html',results=results)






if __name__ == '__main__':
    app.run()
