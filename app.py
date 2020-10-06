from flask import Flask, render_template, request, session, logging, url_for, redirect
from sqlaclhemy import create_engine
from sqlaclhemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

@app.route("/")
def index():
    return 'Olá Mundo!'

if __name__ == "__main__":
    app.run()