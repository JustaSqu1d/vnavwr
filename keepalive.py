from fastapi import FastAPI
from replit import db
from pydantic import BaseModel
from constants import Ships, modes, categories, places
from threading import Thread
from os import system
from fastapi.middleware.cors import CORSMiddleware

def keepalive():
    api = Thread(target=system, args=("uvicorn keepalive:app --host 0.0.0.0",))
    api.start()

class Body(BaseModel):
    ship: str
    mode: str
    category: str
    place: str

app = FastAPI(
    title="Vnav.io World Records API",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://vnav.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=203)
def home():
    return
    

@app.post("/api")
def api(body: Body):
    if body.ship not in Ships:
        return {"error":"Invalid ship.","Valid ships":" | ".join(Ships)}
    if body.mode not in modes:
        return {"error":"Invalid gamemode.","Valid gamemodes":" | ".join(modes)}
    if body.category not in categories:
        return {"error":"Invalid category.","Valid categories":" | ".join(categories)}
    if body.place not in places:
        return {"error":"Invalid place.","Valid places":" | ".join(places)}
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