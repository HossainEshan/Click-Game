@echo off

python -m venv venv

call venv\Scripts\activate

pip install -r requirements.txt

flask db init
flask db migrate -m "Initial migration"
flask db upgrade