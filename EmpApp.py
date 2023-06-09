from flask import Flask, render_template, request, redirect, flash
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
table = 'LeaveList'

# Index
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

# About Us
@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com')

# View Leave List
@app.route("/ViewLeave", methods=['GET'])
def viewLeave():
    cursor = db_conn.cursor() 
    cursor.execute("SELECT * FROM LeaveList")
    leave = cursor.fetchall()
    cursor.close()
    print(leave)
    return render_template('ViewLeave.html', leave = leave)

# Apply Leave
@app.route("/addLeave", methods=['POST', 'GET'])
def addLeave():

    if request.method == 'GET':
        return render_template('addLeave.html')

    if request.method == 'POST':
        leaveId = request.form['leaveId']
        name = request.form['name']
        startDate = request.form['startDate']
        duration = request.form['duration']
        reason = request.form['reason']

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
            check_sql = "SELECT * FROM LeaveList WHERE leaveId = %s"
            cursor.execute(check_sql, leaveId)
            result = cursor.fetchone()

            if result:
                error_msg = "Leave with this ID already exists"
                return render_template('addLeave.html', error_msg=error_msg, leaveId=leaveId, name=name, startDate=startDate, duration=duration, reason=reason)

            insert_sql = "INSERT INTO LeaveList (leaveId, name, startDate, duration, reason) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_sql, (leaveId, name, startDate, duration, reason))
            db_conn.commit()
            
        finally:
            cursor.close()
        print("Leave Applied Successfully...")
        return render_template('addLeaveOutput.html', name=name)

# Edit Leave
@app.route("/editLeave/<string:leaveId>", methods=['POST', 'GET'])
def EditLeave(leaveId):
    if request.method == 'GET':
        cursor = db_conn.cursor()
        cursor.execute("SELECT * FROM LeaveList WHERE leaveId=%s", (leaveId))
        leave = cursor.fetchone()
        cursor.close()

        # Pass leaveList record to EditLeave template
        return render_template('editLeave.html', leave=leave)

    if request.method == 'POST':
        name = request.form['name']
        startDate = request.form['startDate']
        duration = request.form['duration']
        reason = request.form['reason']

        if name == "":
            return "Please enter a name!"
        
        if startDate == "":
            return "Please select a date!"
        
        if int(duration) < 0:
            return "Please select at least 1 day!"
        
        if reason == "":
            return "Please provide a reason!"

        update_sql = "UPDATE LeaveList SET name=%s, startDate=%s, duration=%s,reason=%s WHERE leaveId=%s"
        cursor = db_conn.cursor()

        cursor.execute(update_sql, (name, startDate, duration, reason, leaveId))
        db_conn.commit()
        cursor.close()

        print("Update Leave Successfully...")
        return redirect('/ViewLeave')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
