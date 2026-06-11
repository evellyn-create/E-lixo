from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/faleconosco')
def faleconosco():
    return render_template('faleconosco.html')

@app.route('/gestaodedescarte')
def gestaodedescarte():
    return render_template('gestaodedescarte.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

