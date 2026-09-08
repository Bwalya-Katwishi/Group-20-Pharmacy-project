@echo off
cd /d "%~dp0"
echo Starting PharmaPoint Pharmacy POS...
python -m pip install -r requirements.txt
python run.py
pause
