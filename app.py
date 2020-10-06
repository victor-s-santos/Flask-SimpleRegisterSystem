import pymysql
from functools import wraps
from flask import Flask, render_template, request, session, logging, url_for, redirect, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from passlib.hash import sha256_crypt

engine = create_engine("mysql+pymysql://root:senha@localhost/registro")
                        #mysql+pymysql://usuario:senha@localhost/nome_do_bancodedados
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

#login requered
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged in' in session:
            return f(*args, **kwargs)
        else:
            flash("Login necessário!", 'danger')
            return redirect(url_for('login'))
    return wrap
    #return decorated_function


@app.route("/")
@app.route("/home")
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
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        usuario_get = db.execute("SELECT usuario FROM usuarios2 WHERE usuario=:usuario", {"usuario": usuario}).fetchone()
        senha_get = db.execute("SELECT senha FROM usuarios2 WHERE usuario=:usuario", {"usuario": usuario}).fetchone()

        if usuario_get is None:
            flash("Usuário não encontrado!", "danger")
            return render_template("login.html")
        else:
            for s in senha_get:
                if sha256_crypt.verify(senha, s):
                    session["log"] = True
                    flash("Você está logado!", "success")
                    return redirect(url_for("usuario_logado"))
                else:
                    flash("Senha incorreta!", "danger")
                    return render_template("login.html")

        return render_template("login.html")
    else:
        return render_template("login.html")

#usuario
@app.route("/usuario")
@login_required
def usuario_logado():
    return render_template("usuario.html")

#logout
@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Você está deslogado!", "success")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.secret_key = "flaskehdemais"
    app.run(debug=True)
