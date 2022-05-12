Dev config of Video uploader web app

Prereq: Install MongoDB locally
change app.config["MONGO_URI"] = "mongodb://localhost:27017/pymongo", in app.py of backend accordingly

Start backend:
1.) Navigate to backend folder.
3.) Create a virtualenv : python3 -m venv env
2.) activate venv: source env/bin/activate
3.) Install requirements: pip3 install -r requirements.txt
4.) start flask server: python3 -m flask run.

Start frontend:
1.) Open frontend folder
2.) Install angular dependencies: npm install
3.) Serve angular app: ng serve

Navigate to the app location localhost:4200 and upload videos to view and convert them to grayscale. 
