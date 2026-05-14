@echo off
echo ==========================================
echo   HomeFixr - Starting Backend Server
echo ==========================================
echo.
echo Installing required libraries...
pip install flask flask-cors mysql-connector-python
echo.
echo Starting server...
echo Open browser and go to: http://localhost:5000
echo.
python app.py
pause
