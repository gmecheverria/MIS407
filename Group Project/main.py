from flask import Flask, session, request, render_template, redirect
import secrets, hashlib, sqlite3

app = Flask(__name__)
#flask.session requires a secret_key to run.
#It's set to the random result of secrets.token_bytes() because while testing the program, it would pain to repeatedly clear cookies.
app.secret_key = secrets.token_bytes()

@app.route('/')
def root():
    if "StuID" in session:
        return redirect("/home")
    else:
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if "StuID" in session:
        return redirect("/home")
    elif request.method == "POST":
        netid = request.form.get("NetID")
        passw = request.form.get("passw")
        passh = hashlib.sha1(bytes(passw, "utf-8")).hexdigest()
        conn = sqlite3.connect("database/residence.db")
        curs = conn.cursor()
        curs.execute("SELECT * FROM Student WHERE NetID = '" + netid + "'")
        row = curs.fetchone()
        if(passh == row[6]):
            session["StuID"] = str(row[0])
            session["NetID"] = str(row[1])
            session["Fname"] = str(row[2])
            session["Lname"] = str(row[3])
            session["Pname"] = str(row[4])
            session["Phone"] = str(row[5])
            curs.execute("SELECT * FROM Contract WHERE StuID = '" + session["StuID"] + "'")
            row = curs.fetchone()
            session["Bldg"] = str(row[1])
            session["Room"] = str(row[2])
            session["Bdrm"] = str(row[3])
            session["Pet"] = int(row[4])
            return redirect("/home")
        else:
            return redirect("/login")
    else:
        return render_template("login.html")

@app.route("/home")
def home():
    if "StuID" not in session and request.method == "GET":
        return redirect("/login")
    elif "StuID" in session and request.method == "GET":
        return render_template("home.html", NetID = session["NetID"], CheckInDate = session["CheckInDate"] if "CheckInDate" in session else "Never", CheckOutDate = session["CheckOutDate"] if "CheckOutDate" in session else "Never")
    elif "StuID" in session and request.method == "POST":
        return "filler"
    else:
        return redirect("/login")

@app.route("/check_in", methods=["GET", "POST"])
def check_in():
    if "StuID" not in session:
        return redirect("/login")
    elif "StuID" in session and request.method == "GET":
        return render_template("check_in_form.html", Lname = session["Lname"], Fname = session["Fname"], Pname = session["Pname"],
                                                     StuID = session["StuID"], Email = session["NetID"]+"@iastate.edu", Phone = session["Phone"],
                                                     Bldg = session["Bldg"], Room = session["Room"], Bdrm = session["Bdrm"],
                                                     YesPet = "checked" if session["Pet"] == 1 else "", NoPet = "checked" if session["Pet"] == 0 else "")
    elif "StuID" in session and request.method == "POST":
        data = (session["StuID"], request.form.get("preferred_name"), request.form.get("phone_number"), request.form.get("student_signature"), request.form.get("date"))
        session["Pname"] = request.form.get("preferred_name")
        session["Phone"] = request.form.get("phone_number")
        session["CheckInDate"] = request.form.get("date")
        conn = sqlite3.connect("database/residence.db")
        curs = conn.cursor()
        curs.execute("INSERT INTO CheckIn VALUES (?, ?, ?, ?, ?)", data)
        conn.commit()
        return redirect("/home")
    else:
        return redirect("/home")

@app.route("/check_out", methods=["GET", "POST"])
def check_out():
    if "StuID" not in session:
        return redirect("/login")
    elif "StuID" in session and request.method == "GET":
        return render_template("check_out_form.html", Lname = session["Lname"], Fname = session["Fname"], Pname = session["Pname"],
                                                      StuID = session["StuID"], Email = session["NetID"]+"@iastate.edu", Phone = session["Phone"],
                                                      Bldg = session["Bldg"], Room = session["Room"], Bdrm = session["Bdrm"],
                                                      YesPet = "checked" if session["Pet"] == 1 else "", NoPet = "checked" if session["Pet"] == 0 else "")
    elif "StuID" in session and request.method == "POST":
        data = (session["StuID"], request.form.get("preferred_name"), request.form.get("phone_number"), request.form.get("student_signature"), request.form.get("date"))
        session["Pname"] = request.form.get("preferred_name")
        session["Phone"] = request.form.get("phone_number")
        session["CheckOutDate"] = request.form.get("date")
        #conn = sqlite3.connect("database/residence.db")
        #curs = conn.cursor()
        #curs.execute("INSERT INTO CheckOut VALUES (?, ?, ?, ?, ?)", data)
        #conn.commit()
        return redirect("/home")
    else:
        return redirect("/home")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
