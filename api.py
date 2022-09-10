from os import system
from threading import Thread

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal

from constants import bot


def api_run():
    client = Thread(target=system, args=("uvicorn api:app --host 0.0.0.0 --port 8080",))
    client.start()


class Body(BaseModel):
    ship: Literal[
        "Alien Blaster",
        "Annihilator",
        "Artillery",
        "Eagle",
        "Astronaut",
        "Auto 4",
        "Auto 5",
        "Barricade",
        "Basic",
        "Bat",
        "Bomber",
        "Boomerang",
        "Boomertwin",
        "Booster",
        "Boosterflip",
        "Builder",
        "Bushwacker",
        "Carrier",
        "Conqueror",
        "Cruiser",
        "Demolisher",
        "Drone Addict",
        "Drone Trapper",
        "Dual",
        "Factory",
        "Fighter",
        "Flank Guard",
        "Fortress",
        "Galaxian",
        "Gunner",
        "Gunner Trapper",
        "Hulk",
        "Hunter",
        "Hybrid",
        "Machine Gun",
        "Mega 3",
        "Necromancer",
        "Octo Ship",
        "Falcon",
        "Overboomerang",
        "Overgunner",
        "Overlord",
        "Polyballs",
        "Power Glider",
        "Predator",
        "Quad Ship",
        "Quad-builder",
        "Quadlet",
        "Quintlet",
        "Ranger",
        "Savage",
        "Skimmer",
        "Sniper",
        "Space Jet",
        "Spike",
        "Sprayer",
        "Sputnik",
        "Stradblock",
        "Streamliner",
        "Surfer",
        "Trappershot",
        "Trappetytrap",
        "Triple Twin",
        "Triplet",
        "Twin Flank",
        "Twin Laser",
        "UFO",
    ]
    mode: Literal["FFA", "2 Teams"]
    category: Literal["Fast 500k", "Fast 1m", "Fast 1,5m", "High Score"]
    place: Literal[
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "Mobile 1st",
        "Mobile 2nd",
        "Mobile 3rd",
    ]


app = FastAPI(title="Vnav.io World Records API", version="1.1.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=203)
async def home():
    return


@app.post("/api")
async def api(body: Body):
    db = bot.db.find_one({"Name": "WR"})
    try:
        data = data
        result = {
            "user_id": data[
                "user"
            ].split("|")[0],
            "score": data["user"].split(
                "|"
            )[1],
            "link": data["link"],
            "hours": data["hour"],
            "minutes": data["min"],
            "seconds": data["sec"],
        }
    except:
        result = {
            "user_id": 0,
            "score": 0,
            "link": 0,
            "hours": 0,
            "minutes": 0,
            "seconds": 0,
        }
    return result
