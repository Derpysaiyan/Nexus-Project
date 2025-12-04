Open the Terminal in the Nexus Backend Folder
(i prefer using git bash, opens the venv immediately)
if bash does not open the venv, run:
source venv/Scripts/activate

if using git bash 


1. 
cd "Nexus Backend" 
Ensures your Terminal is in the correct spot

2. 
pip install -r requirements.txt

All the needed files

3. 
python app.py

opens the backend and can be opened at 
http://127.0.0.1:5000/

4. Run the frontend with "live server", the extension is on vscode and open it at catalog
(so far the part which i have working with the db)
http://127.0.0.1:5500/catalog.html
is the frontend catalog


http://127.0.0.1:5000/Products
is the Product's database in real time asssuming both frontend and backend are running


if using powershell Terminal
1. 
cd "Nexus Backend" 
ensures your in the correct 


2. 

.\venv\Scripts\Activate.ps1


activates the venv, but if Scripts is blocked use 
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass



3.

pip install -r requirements.txt



4. 
python app.py

# nothing