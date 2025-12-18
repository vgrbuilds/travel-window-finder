from database import SessionLocal, engine, Base
from models import RoadClosure, TrafficPattern
from datetime import date

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    road_closures = [
        RoadClosure(location="Chikmagalur", start_date=date(2025, 8, 15), end_date=date(2025, 8, 17), reason="Maintenance"),
        RoadClosure(location="Coorg", start_date=date(2025, 8, 20), end_date=date(2025, 8, 22), reason="Festival"),
        RoadClosure(location="Sakleshpur", start_date=date(2025, 8, 25), end_date=date(2025, 8, 26), reason="Construction"),
    ]

    for closure in road_closures:
        db.add(closure)

    locations = ["Chikmagalur", "Coorg", "Sakleshpur"]
    for location in locations:
        for day in range(7):
            score = 5.0 + (day % 3) * 1.5
            traffic = TrafficPattern(location=location, day_of_week=day, traffic_score=min(10.0, score))
            db.add(traffic)

    db.commit()
    db.close()

if __name__ == "__main__":
    seed_data()
    print("Database seeded successfully!")
