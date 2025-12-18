# Travel Window Finder

A full-stack application to find the best consecutive travel dates for 1–3 destinations based on weather, road closures, and traffic patterns.

## Features

- **Frontend**: Single-page React chat interface for user input and displaying recommendations.
- **Backend**: FastAPI service that parses user messages, fetches weather data, checks road closures and traffic, and computes optimal travel windows.
- **Database**: SQLite with dummy data for road closures and traffic patterns.

## Quick Start

Run the entire application with one command:
```
start.bat
```

This will start both the backend (http://localhost:8000) and frontend (http://localhost:3000) servers.

## Manual Setup Instructions

### Backend

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment (if not already created):
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```
   venv\Scripts\activate  # On Windows
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Seed the database:
   ```
   python seed_data.py
   ```

6. Run the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

The backend will be available at `http://localhost:8000`.

### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the React app:
   ```
   npm start
   ```

The frontend will be available at `http://localhost:3000`.

## Usage

1. Start both backend and frontend servers.
2. In the frontend, enter a message like: "I want to travel to Chikmagalur, Coorg and Sakleshpur for 5 days. What are the best conditions?"
3. Click "Find Best Window" to get recommendations.

## Scoring Logic

The scoring system (0-10) penalizes:
- Rainy days: -1 per day
- Stormy days: -2 per day
- Road closures: -3
- High traffic (score >7): -0.5 per point above 7

Higher scores indicate better travel conditions.

## API Endpoint

- `POST /travel/recommend`: Accepts a JSON with `message` field, returns travel recommendations.
