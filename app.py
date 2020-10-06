import pymysql
from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt

engine = create_engine("mysql+pymysql://root:senha@localhost/registro")
                        #mysql+pymysql://usuario:senha@localhost/nome_do_bancodedados
db = scoped_session(sessionmaker(bind=engine))

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
        #to ensure password secure
        secure_password = sha256_crypt.encrypt(str(senha))

        if senha == confirma:
            db.execute("INSERT INTO usuarios2(nome, usuario, senha) VALUES(:nome, :usuario, :senha)",
                                            {"nome":nome, "usuario":usuario, "senha":secure_password})
            db.commit()
            flash("Usuário registrado com sucesso, já é possível realizar o Login!", "success")
            return redirect(url_for('login'))
        else:
            flash("Infelizmente as senhas não conferem!", "danger")
            return render_template("register.html")

    return render_template("register.html")

#login form
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return render_template("login.html")
    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.secret_key = "flaskehdemais"
    app.run(debug=True)
