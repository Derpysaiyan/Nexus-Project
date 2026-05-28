Using the Code locally:
	The file should come with the 2 main files, 
    Nexus Backend, and phone-frontend. 
    To run locally you must first first open a terminal to run the code, 
    so open up git bash, the preferred terminal in this case to run ‘ignore brackets’ 
    [cd (“Nexus Backend”)] and this will take you to the correct folder space. 
    Afterwards, you can run [pip install -r requirements.txt] to install all imported files and such needed to run the software, 
    should be something like this:
blinker==1.9.0
click==8.3.1
colorama==0.4.6
Flask==3.1.2
flask-cors==6.0.1
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
Werkzeug==3.1.4
gunicorn==22.0.0

After that you’ll want to determine whether you have a file named (Nexus.db), 
this file is the database and should be deleted when deploying on a frontend server, 
but for usage on the backend, it’s needed to load in all product files. Now to create this file, you need to run 

[py Nexus_db.py] and it’ll run that file and create an EMPTY database. Then you can run

[py seed_data.py] which will seed all the needed data in the db. 
Afterwards you can run the actual backend which runs on flask, 

[py app.py] and you should get a link in terminal letting you know you have the backend running.

Now for the frontend, you need to run it live, for our usage it was done with the VScode extension, 
“Live server” and it should give you a button on the bottom right. Open the file, catalog.html, 
this serves as our homepage and click “go live” at the bottom right and it should open up the file. 
Now if everything is working properly you should have the website running locally, 
but it’s imperative to delete the Nexus.db when making updates to the code on the actual live server running on github, 
it will create it’s own db and use that to update changes. 
Locally though you’d want to delete it if you wantedf to quickly reset the data, 
though you’d have to reseed it again using the same steps of creating and seeding. 

Using the Code live: https://nexus-frontend-w6yo.onrender.com 
	The Live server was made using Render, so it’s currently connected on github and any changes made to github reflect on the server. 
    The server uses a free plan so it does not allow us to use the shell. 
    The live server runs in the same manner using the 2 files to create a static site the frontend and a web service the backend. 
    For the backend, it requires a file named render.yaml
And without this it won’t run. 
the render.yaml contians
services:
  - type: web       # The type being a web API
    name: nexus-backend   # The name you want to see on Render dashboard
    runtime: python       # Tell Render you’re using Python
    buildCommand: pip install -r requirements.txt   # Install dependencies
    startCommand: gunicorn app:app                  # Start your server
    envVars:
      - key: PYTHON_VERSION
        value: 3.10

It essentially gives instructions on how to run the service and in what order, all it’s dependencies. 
For the frontend, it looks for a file named Index.html which needs to instruct it what it needs to open,
the rest is managed like normal, and right now it’s set to open the Catalog.html as that's essentially our homepage. 
One feature that was added as well, since we do not have access to the shell on Render, we cannot delete the database normally. 
So in order to delete this, you must run 

fetch("https://nexus-project-webserver.onrender.com/admin/reset-db", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ key: "Reset123!" })
})
  .then(r => r.json())
  .then(console.log);

This is essentially a method made in app.py to delete the db, 
use the key created in the Nexus-Project render environments, 
Key is ADMIN_RESET_KEY, and value is Reset123!, can be changed. In order to run this command,
you need to open any webpage, inspect and click or press f12, and then you can run this command in the console to fetch the server link, 
use the delete method, and insert the Reset key, and you should get confirmation it was reseeded. 


Helpful methods to visualize the data are
https://nexus-project-webserver.onrender.com/Products
https://nexus-project-webserver.onrender.com/Users
https://nexus-project-webserver.onrender.com/Orders
https://nexus-project-webserver.onrender.com/Orders/user/1
https://nexus-project-webserver.onrender.com/Brand
https://nexus-project-webserver.onrender.com
