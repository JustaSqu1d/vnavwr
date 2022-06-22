from fastapi import FastAPI, Path
from replit import db
from pydantic import BaseModel
from constants import Ships, modes, categories, places

class Body(BaseModel):
    ship: str
    mode: str
    category: str
    place: str

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Use https://vnavwr.squidsquidsquid.repl.co/docs for some information"} 

@app.get("/api")
def api(body: Body):
    if body.ship not in Ships:
        return {"error":"Invalid ship."}
    if body.mode not in modes:
        return {"error":"Invalid gamemode."}
    if body.category not in categories:
        return {"error":"Invalid category."}
    if body.place not in places:
        return {"error":"Invalid place."}
    try:
        dict = {
            "user_id": db[body.ship][body.mode][body.category][body.place]["user"].split("|")[0],
            "score": db[body.ship][body.mode][body.category][body.place]["user"].split("|")[1],
            "link": db[body.ship][body.mode][body.category][body.place]["link"],
            "hours": db[body.ship][body.mode][body.category][body.place]["hour"],
            "minutes": db[body.ship][body.mode][body.category][body.place]["min"],
            "seconds": db[body.ship][body.mode][body.category][body.place]["sec"]
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
    return dict