@echo off
echo Starting Travel Window Finder Application...

cd backend
start cmd /k "venv\Scripts\activate && python seed_data.py && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 5 /nobreak > nul

cd ..\frontend
start cmd /k "npm start"

echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo Press any key to exit this window (servers will continue running)
pause > nul
