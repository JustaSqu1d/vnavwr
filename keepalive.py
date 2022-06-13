from flask import Flask, Response, request, jsonify, render_template
from threading import Thread
from replit import db
from constants import Ships, modes, categories, places


app = Flask("")

@app.route("/")
def home():
  return "Use https://vnavwr.squidsquidsquid.repl.co/api"

@app.route("/api/", methods=['GET', 'POST'])
def api():
    data = request.get_json()
    if data == None:
        return Response(
            mimetype="application/json",
            response={"Bad Request Body.":"Use https://vnavwr.squidsquidsquid.repl.co/docs for some information"},
            status=400
        )
        
    ship, mode, category, place = str(data["ship"]), str(data["mode"]), str(data["category"]), str(data["place"])
    if ship not in Ships:
        return jsonify(
            {"error":"Invalid ship."}
        )
    if mode not in modes:
        return jsonify(
            {"error":"Invalid gamemode."}
        )
    if category not in categories:
        return jsonify(
            {"error":"Invalid category."}
        )
    if place not in places:
        return jsonify(
            {"error":"Invalid place."}
        )
    try:
        dict = {
            "user_id": db[ship][mode][category][place]["user"].split("|")[0],
            "score": db[ship][mode][category][place]["user"].split("|")[1],
            "link": db[ship][mode][category][place]["link"],
            "hours": db[ship][mode][category][place]["hour"],
            "minutes": db[ship][mode][category][place]["min"],
            "seconds": db[ship][mode][category][place]["sec"]
        }
    except:
        dict = {
            "user_id": 0,
            "score": 0,
            "link": 0,
            "hours": 0,
            "minutes": 0,
            "seconds": 0
        }
    return jsonify(dict)

@app.route("/docs")
def docs():
    return render_template("docs.html")

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()