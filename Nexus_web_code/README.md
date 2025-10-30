ReadME Documentation



1. Unzip the folder.


2. Open a terminal in the unzipped folder (where manage.py is).


3. Create/activate venv:
Windows PowerShell (run these commands):

python -m venv venv

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\venv\Scripts\Activate.ps1


macOS/Linux:

python -m venv venv

source venv/bin/activate


Afterwards Run: 
Install deps: pip install -r requirements.txt

Init DB: python manage.py migrate

(Optional) Admin user: python manage.py createsuperuser


Run: python manage.py runserver → open http://127.0.0.1:8000/

For seed_store.json: 

python manage.py migrate
python manage.py loaddata seed_store.json
python manage.py runserver
