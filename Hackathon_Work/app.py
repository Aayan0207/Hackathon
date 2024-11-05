from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
import secrets
from functools import wraps
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = 6000
app.config["SECRET_KEY"] = secrets.token_hex(16)
Session(app)

mydb = mysql.connector.connect(
    host="localhost",
    user="root", #Change username accordingly please
    password="Leonardo@28", #Updated password for user
    database="hackathon" #In case name wasn't kept as hackathon while setup kindly change this to the new name
)
cursor_log = mydb.cursor()
cursor_discuss = mydb.cursor()
cursor_tasks=mydb.cursor()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") == "Not Logged In" or not session.get("user"):
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return render_template("main.html", user=session.get("user", "Not Logged In"))


@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    cursor_tasks.execute("SELECT Author,Tasks,Urgency FROM tasks ORDER BY Urgency DESC")
    session["tasks"] = cursor_tasks.fetchall()
    if request.method == "GET":
        return render_template("tasks.html", user=session["user"],tasks=session['tasks'])
    elif request.method == "POST":
        task=request.values.get('task')
        urgency=request.values.get('urgency')
        if not task:
            task=""
            urgency=1
        else:
            cursor_tasks.execute('INSERT INTO tasks (Author,tasks,urgency) Values (%s,%s,%s)',(session['user'],task,urgency))
            mydb.commit()
            return jsonify({"user":session['user'],"new_task":(session['user'],task,urgency)})


@app.route("/discuss", methods=["GET", "POST"])  
@login_required
def discuss():
    cursor_discuss.execute("SELECT Author,Message FROM discussion")
    session["discuss"] = cursor_discuss.fetchall()
    if request.method == "GET":
        return render_template(
            "discuss.html", user=session["user"], discussion=session["discuss"]
        )
    elif request.method == "POST":
        message = request.values.get("message")
        if not message:
            message = ""
        else:
            cursor_discuss.execute(
                "INSERT INTO discussion (Author, Message) VALUES (%s,%s)",
                (session["user"], message),
            )
            mydb.commit()
        return jsonify(
            {"user": session["user"], "new_message": (session["user"], message)}
        )


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    session["string"] = ""
    session["user"] = "Not Logged In"
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username_reg = request.values.get("username_reg")
        password_reg = request.values.get("password_reg")
        confirmation = request.values.get("repassword")
        if password_reg != confirmation:
            session["string"] = "Password and Confirm Password don't match"
            return jsonify({"string": session["string"], "user": session["user"]})
        cursor_log.execute("SELECT * FROM data where username=%s", (username_reg,))
        result = cursor_log.fetchall()
        if len(result) != 0:
            session["string"] = "Username already taken."
            return jsonify({"string": session["string"], "user": session["user"]})
        cursor_log.execute(
            "INSERT INTO data (username,password) values(%s,%s)",
            (username_reg, generate_password_hash(password_reg)),
        )
        mydb.commit()
        session["user"] = username_reg.capitalize()
        session["string"] = "Registration Successful"
        return jsonify({"string": session["string"], "user": session["user"]})


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    session["string"] = ""
    session["user"] = "Not Logged In"
    if request.method == "GET":
        return render_template("login.html", user="Not Logged In")
    elif request.method == "POST":
        username_log = request.values.get("username_log")
        password_log = request.values.get("password_log")
        cursor_log.execute("SELECT * FROM data WHERE username=%s", (username_log,))
        result = cursor_log.fetchall()
        if len(result) != 1 or not check_password_hash(result[0][2], password_log):
            session["string"] = "Username and/or Password is incorrect."
            return jsonify({"string": session["string"], "user": session["user"]})
        session["user"] = username_log.capitalize()
        session["string"] = "Login Successful"
        return jsonify({"string": session["string"], "user": session["user"]})

@app.route('/delete_task',methods=['POST'])
def delete():
    author=request.values.get('del_author').strip(':')
    task=request.values.get('del_task').strip()
    urgency=request.values.get('del_urgency')
    cursor_tasks.execute('DELETE FROM tasks WHERE author=%s AND tasks=%s AND urgency=%s',(author,task,urgency))
    mydb.commit()
    return redirect('/tasks') 

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
