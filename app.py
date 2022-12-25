from flask import Flask, request, session, render_template, jsonify
from flask_cors import CORS

from flask_mysqldb import MySQL
import MySQLdb.cursors
import flask_cors
import re

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Vamshi@555'
app.config['MYSQL_DB'] = 'agri'

mysql = MySQL(app)

CORS(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    args = request.args
    username = args["username"]
    password = args["password"]
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = f'SELECT * from users where users.username ="{username}" and users.password="{password}"'
    print(query)
    cursor.execute(query)
    return jsonify(cursor.fetchone())



@app.route('/signup', methods=['GET'])
def signup():
    args = request.args
    username = args["email"]
    password = args["password"]
    phone = args["phone"]
    name1 = args["name"]
    address = args["address"]
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = f"INSERT INTO users VALUES (NULL, '{username}', '{password}', '{phone}', '{address}', '{name1}')"
    print(query)
    cursor.execute(query)
    mysql.connection.commit()

    return "OK"




@app.route('/forrent', methods=['GET'])
def forrent():
    args = request.args
    user_id = args["user_id"]
    equipment_id = args["equipment_id"]
    rent_per_day = args["rent_per_day"]
    advance = args["advance"]
    from_date = args["from_date"]
    to_date = args["to_date"]
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = f"INSERT INTO forrent VALUES (NULL, {equipment_id}, {user_id}, {rent_per_day}, {advance}, {from_date}, {to_date})"
    print(query)
    cursor.execute(query)
    mysql.connection.commit()

    return "OK"


@app.route('/torent', methods=['GET', 'POST'])
def torent():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = f'SELECT * from forrent'
    print(query)
    cursor.execute(query)
    pp = cursor.fetchall()
    stringss=[]
    print(pp)
    for i in pp:
        query=f'SELECT * from users where id={i["user_id"]}'
        cursor.execute(query)
        u=cursor.fetchone()
        email, phone, address, name = u["username"],u["phone"],u["address"],u["name"]
        query = f'SELECT name from equipment where id={i["equipment_id"]}'
        cursor.execute(query)
        e = cursor.fetchone()
        stringss.append([e["name"], name,i["rent_per_day"],i["rent_per_day"]*10,i["advance"],i["start_date"],i["end_date"],phone,email, address])
    return render_template("ht.html", data=stringss)
