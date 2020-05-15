# Author: Femke Spaans
# Date: 07-05-2020
# Name: Afvink 3
# Version: 1

from flask import Flask, render_template, request, redirect, \
    url_for, session, flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "kuikens"


@app.route('/login', methods=["POST", "GET"])
def user_name():
    if request.method == "POST":
        user_name = request.form.get("username", "")
        password = request.form.get("password", "")
        session["henk"] = user_name
        session["wachtwoord"] = password
        try:
            get_myMessages(user_name, password)
        except mysql.connector.Error as err:
            if "Access denied" in err.msg:
                flash("Invalid credentials")
                return render_template("afvink3B.html")
        return redirect(url_for("messages"))
    else:
        return render_template("afvink3B.html")


@app.route('/')
def home():
    return redirect(url_for("user_name"))


@app.route('/database_piep', methods=["POST", "GET"])
def messages():
    messages = ""
    search_word = "" 
    if request.method == "POST":
        user_name = session["henk"]
        password = session["wachtwoord"]
        search_word = request.form.get("Messages")
        messages = filterMessage(user_name, password, search_word)
    return render_template("afvink3B1.html", messages=messages, filter=search_word)


def get_myMessages(user_name, password):
    conn = mysql.connector.connect(
        host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
        user="fxfke@hannl-hlo-bioinformatica-mysqlsrv",
        database=user_name,
        password=password)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT piep.bericht, "
        "student.voornaam, "
        "student.tussenvoegsels, "
        "student.achternaam "
        "FROM piep, student "
        "WHERE student.student_nr = piep.student_nr "
        "ORDER BY piep_id ASC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def filterMessage(user_name, password, search_word):
    conn = mysql.connector.connect(
        host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com",
        user="fxfke@hannl-hlo-bioinformatica-mysqlsrv",
        database=user_name,
        password=password)
    cursor = conn.cursor()
    search_word = search_word.replace("#", "").replace("\'", "")
    cursor.execute("SELECT piep.bericht, "
                   "student.voornaam, "
                   "student.tussenvoegsels, "
                   "student.achternaam "
                   "FROM piep, student "
                   "WHERE student.student_nr = piep.student_nr "
                   "AND bericht LIKE '%" + search_word + "%'")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows




if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
