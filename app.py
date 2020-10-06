from flask import Flask, render_template, request, session, logging, url_for, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home.html')

#registration form
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form.get("nome")
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        confirma = request.form.get("confirm")

        if senha == confirma:
            print('É igual')
    return render_template("register.html")

#login form
@app.route("/login")
def login():
    if request.method == "POST":
        return render_template("login.html")
    else:
        return(request.method)

if __name__ == "__main__":
    app.run(debug=True)