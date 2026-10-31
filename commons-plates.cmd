@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
rem Candidats Wikimedia Commons (licences libres) pour les pays a moins de 2 plaques : lent, mis en cache
where py >nul 2>nul
if %errorlevel%==0 (py tools\fetch_commons_plates.py %*) else (python tools\fetch_commons_plates.py %*)
if exist _commons\review.html start "" "_commons\review.html"
pause
