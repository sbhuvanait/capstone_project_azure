import os
import sys 
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import pyodbc

app = Flask(__name__)

# Create connection to Azure SQL
def sqlConnection():
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=socgensqlserver.database.windows.net;Database=b-admin;uid=socgen-admin;pwd=Pa$$w0rd123$')
    cursor = conn.cursor()
    print('connection established')
    return cursor

def writeToJson(rows):
    data = []
    for i in rows:
        data.append(list(i))
    return json.dumps(data)

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/all_categories')
def get_all_categories():
    cur = sqlConnection()
    row = cur.execute("select * from category")
    rows = cur.fetchall()
    data = writeToJson(rows)
    cur.close()
    return data

@app.route('/add_new_category', methods=['POST'])
def add_new_category():
    cur = sqlConnection()

    content = request.get_json()
    print(content)
    data = content
    for key, value in data.items():
        print(key, value)
        if key == 'id':
            print( value)
            idVal = value
        elif key == 'name':
            print('inside 2=> '+value)
            nameVal = value

    cur.execute("insert into category (id, name) values (%s, '%s');" %(idVal, nameVal ))
    cur.commit()
    cur.close()
    return "Rows are inserted"

@app.route('/update_category', methods=['PUT'])
def update_category():
    cur = sqlConnection()
    content = request.get_json()
    print(content)
    data = content
    for key, value in data.items():
        print(key, value)
        if key == 'id':
            idVal = value
        elif key == 'name':
            nameVal = value

    cur.execute("update category set name = '%s' where id = %s;" %( nameVal, idVal ))
    cur.commit()
    cur.close()
    return "Rows has been updated"

@app.route('/delete_category', methods=['DELETE'])
def delete_category():
    cur = sqlConnection()
    content = request.get_json()
    print(content)
    data = content
    for key, value in data.items():
        print(key, value)
        if key == 'id':
            idVal = value
    cur.execute("delete from category where id = %s;" %( idVal ))
    cur.commit()
    cur.close()
    return "Rows has been deleted"

#################################Author###############################

@app.route('/all_authors')
def get_all_authors():
    cur = sqlConnection()
    row = cur.execute("select * from author")
    rows = cur.fetchall()
    data = writeToJson(rows)
    cur.close()
    return data

@app.route('/add_new_author', methods=['POST'])
def add_new_author():
    cur = sqlConnection()

    content = request.get_json()
    print(content)
    data = content
    for key, value in data.items():
        print(key, value)
        if key == 'id':
            idVal = value
        elif key == 'first_name':
            fnameVal = value
        elif key == 'last_name':
            lnameVal = value

    cur.execute("insert into author (id, first_name, last_name) values (%s, '%s', '%s');" %(idVal, fnameVal, lnameVal ))
    cur.commit()
    cur.close()
    return "Rows are inserted"

@app.route('/update_author', methods=['PUT'])
def update_author():
    cur = sqlConnection()
    content = request.get_json()
    print(content)
    data = content
    for key, value in data.items():
        print(key, value)
        if key == 'id':
            idVal = value
        elif key == 'first_name':
            fnameVal = value
        elif key == 'last_name':
            lnameVal = value

    cur.execute("update author set first_name = '%s', last_name= '%s' where id = %s;" %( fnameVal, lnameVal, idVal ))
    cur.commit()
    cur.close()
    return "Rows has been updated"

@app.route('/delete_author', methods=['DELETE'])
def delete_author():
    cur = sqlConnection()
    content = request.get_json()
    print(content)
    data = content
    for key, value in data.items():
        print(key, value)
        if key == 'id':
            idVal = value
    cur.execute("delete from author where id = %s;" %( idVal ))
    cur.commit()
    cur.close()
    return "Rows has been deleted"


################################LAB###################################

@app.route('/all_labs')
def get_all_labs():
    cur = sqlConnection()
    row = cur.execute("select * from lab")
    rows = cur.fetchall()
    data = writeToJson(rows)
    cur.close()
    return data

@app.route('/add_new_lab', methods=['POST'])
def add_new_lab():
    cur = sqlConnection()

    content = request.get_json()
    print(content)
    data = content
    for key, value in data.items():
        print(key, value)
        if key == 'id':
            idVal = value
        elif key == 'name':
            nameVal = value
        elif key == 'descr':
            descVal = value
        elif key == 'cat_id':
            catVal = value
        elif key == 'auth_id':
            authVal = value

    cur.execute("insert into lab (id, name, description, category_id, author_id) values (%s, '%s', '%s', %s, %s);" %(idVal, nameVal, descVal, catVal, authVal ))
    cur.commit()
    cur.close()
    return "Rows are inserted"

@app.route('/update_lab', methods=['PUT'])
def update_lab():
    cur = sqlConnection()
    content = request.get_json()
    print(content)
    data = content
    for key, value in data.items():
        print(key, value)
        if key == 'id':
            idVal = value
        elif key == 'name':
            nameVal = value
        elif key == 'descr':
            descVal = value

    cur.execute("update lab set name = '%s', description = '%s' where id = %s;" %( nameVal, descVal, idVal ))
    cur.commit()
    cur.close()
    return "Rows has been updated"


@app.route('/delete_lab', methods=['DELETE'])
def delete_lab():
    cur = sqlConnection()
    content = request.get_json()
    print(content)
    data = content
    for key, value in data.items():
        print(key, value)
        if key == 'id':
            idVal = value
    cur.execute("delete from lab where id = %s;" %( idVal ))
    cur.commit()
    cur.close()
    return "Rows has been deleted"

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')
   
   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()