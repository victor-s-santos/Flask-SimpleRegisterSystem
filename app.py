from flask import Flask, render_template, request, session, logging, url_for, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)