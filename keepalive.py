from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return ""

@app.route('/a')
def home1():
  return "a"

@app.route('/b')
def home2():
  return "b"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()