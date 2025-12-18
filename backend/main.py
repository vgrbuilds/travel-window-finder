from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import requests
from datetime import datetime, timedelta
from database import SessionLocal
from models import RoadClosure, TrafficPattern
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TravelRequest(BaseModel):
    message: str

class TravelResponse(BaseModel):
    destinations: List[str]
    duration_days: int
    best_window: dict

def parse_message(message: str):
    destinations_match = re.search(r'travel to (.+?) for (\d+) days', message, re.IGNORECASE)
    if not destinations_match:
        raise HTTPException(status_code=400, detail="Invalid message format")
    
    destinations_str = destinations_match.group(1)
    duration = int(destinations_match.group(2))
    destinations = [d.strip() for d in destinations_str.split(',')]
    
    if len(destinations) > 3 or len(destinations) < 1:
        raise HTTPException(status_code=400, detail="1-3 destinations required")
    
    return destinations, duration

def get_weather_forecast(location: str, start_date: datetime, end_date: datetime):
    coords = {
        "Chikmagalur": (13.32, 75.77),
        "Coorg": (12.34, 75.81),
        "Sakleshpur": (12.94, 75.78)
    }
    lat, lon = coords.get(location, (12.97, 77.59))
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_sum,weathercode&start_date={start_date.date()}&end_date={end_date.date()}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return None
    
    return response.json()['daily']

def check_road_closures(location: str, start_date: datetime, end_date: datetime):
    db = SessionLocal()
    closures = db.query(RoadClosure).filter(
        RoadClosure.location == location,
        RoadClosure.start_date <= end_date.date(),
        RoadClosure.end_date >= start_date.date()
    ).all()
    db.close()
    return len(closures) > 0

def get_traffic_score(location: str, date: datetime):
    db = SessionLocal()
    day_of_week = date.weekday()
    traffic = db.query(TrafficPattern).filter(
        TrafficPattern.location == location,
        TrafficPattern.day_of_week == day_of_week
    ).first()
    db.close()
    return traffic.traffic_score if traffic else 5.0

def calculate_score(destinations: List[str], start_date: datetime, duration: int):
    end_date = start_date + timedelta(days=duration - 1)
    total_score = 10.0
    reasons = []

    for dest in destinations:
        weather = get_weather_forecast(dest, start_date, end_date)
        if weather:
            rain_days = sum(1 for p in weather['precipitation_sum'] if p is not None and p > 0.5)
            storm_days = sum(1 for w in weather['weathercode'] if w is not None and w in [95, 96, 99])
            
            if rain_days > 0:
                total_score -= rain_days * 1.0
                reasons.append(f"{rain_days} rainy days in {dest}")
            if storm_days > 0:
                total_score -= storm_days * 2.0
                reasons.append(f"{storm_days} stormy days in {dest}")
            if rain_days == 0 and storm_days == 0:
                reasons.append(f"Good weather in {dest}")
        else:
            reasons.append(f"Weather data unavailable for {dest}")

        if check_road_closures(dest, start_date, end_date):
            total_score -= 3.0
            reasons.append(f"Road closures in {dest}")
        else:
            reasons.append(f"No road closures in {dest}")

        avg_traffic = sum(get_traffic_score(dest, start_date + timedelta(days=i)) for i in range(duration)) / duration
        if avg_traffic > 7.0:
            total_score -= (avg_traffic - 7.0) * 0.5
            reasons.append(f"High traffic in {dest}")
        else:
            reasons.append(f"Manageable traffic in {dest}")

    return max(0.0, total_score), reasons

@app.post("/travel/recommend", response_model=TravelResponse)
def recommend_travel(request: TravelRequest):
    destinations, duration = parse_message(request.message)
    today = datetime.now()
    best_score = -1
    best_window = None

    for days_ahead in range(30 - duration + 1):
        start = today + timedelta(days=days_ahead)
        score, reasons = calculate_score(destinations, start, duration)
        if score > best_score:
            best_score = score
            best_window = {
                "start_date": start.date().isoformat(),
                "end_date": (start + timedelta(days=duration-1)).date().isoformat(),
                "score": round(score, 1),
                "reasons": reasons
            }

    if not best_window:
        raise HTTPException(status_code=500, detail="No suitable window found")

    return {"destinations": destinations, "duration_days": duration, "best_window": best_window}
