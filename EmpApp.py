from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'Leave'

# Index
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addLeave.html')

# About Us
@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com')


@app.route("/ViewLeave", methods=['GET'])
def viewLeave():
    cursor = db_conn.cursor() 
    cursor.execute("SELECT * FROM Leave")
    leave = cursor.fetchall()
    cursor.close()
    print(leave)
    return render_template('ViewLeave.html', leave = leave)

@app.route("/addLeave", methods=['POST', 'GET'])
def addLeave():

    if request.method == 'GET':
        return render_template('addLeave.html')

    if request.method == 'POST':
        leaveId = int(request.form['leaveId'])
        name = request.form['name']
        startDate = request.form['startDate']
        duration = int(request.form['duration'])
        reason = request.form['reason']

        insert_sql = "INSERT INTO Leave VALUES (%s, %s, %s, %s, %s)"
        cursor = db_conn.cursor()
        
        if name == "":
            return "Please enter a name!"
        
        if startDate == "":
            return "Please select a date!"
        
        if int(duration) < 0:
            return "Please select at least 1 day!"
        
        if reason == "":
            return "Please provide a reason!"

        try:
            # To check if emp_id already exists
            check_sql = "SELECT * FROM Leave WHERE leaveId = %s"
            cursor.execute(check_sql, (leaveId,))
            result = cursor.fetchone()

            if result:
                error_msg = "Leave with this ID already exists"
                return render_template('addLeave.html', error_msg=error_msg, leaveId=leaveId, name=name, startDate=startDate, duration=duration, reason=reason)


            cursor.execute(insert_sql, (leaveId, name, startDate, duration, reason))
            db_conn.commit()
            
        finally:
            cursor.close()
        
        print("Leave Applied Successfully...")
        return redirect('addLeaveOutput.html', name=name)

@app.route("/editLeave/<string:leaveId>", methods=['POST', 'GET'])
def EditLeave(leaveId):
    if request.method == 'GET':
        cursor = db_conn.cursor()
        cursor.execute("SELECT * FROM Leave WHERE leaveId=%s", (leaveId,))
        leave = cursor.fetchone()
        cursor.close()

        # Pass payroll record to EditPayroll template
        return render_template('editLeave.html', leave=leave)

    if request.method == 'POST':
        name = request.form['name']
        startDate = request.form['startDate']
        duration = int(request.form['duration'])
        reason = request.form['reason']

        if name == "":
            return "Please enter a name!"
        
        if startDate == "":
            return "Please select a date!"
        
        if int(duration) < 0:
            return "Please select at least 1 day!"
        
        if reason == "":
            return "Please provide a reason!"

        update_sql = "UPDATE Leave SET name=%s, startDate=%s, duration=%s,reason=%s WHERE leaveId=%s"
        cursor = db_conn.cursor()

        cursor.execute(update_sql, (name, startDate, duration, reason, leaveId))
        db_conn.commit()
        cursor.close()

        print("Update Leave Successfully...")
        return redirect('/ViewLeave')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
