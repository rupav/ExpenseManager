# Local Development Setup.

The instructions on this page will guide you in setting up a local development
environment in Windows OS.

1. Fork this repo, and then clone your forked copy:
Open git terminal(Git bash in windows), and clone your forked repo i.e. `git clone https://github.com/<your_username>/ExpenseManager.git` in the directory you want.
2. Now using cmd or powershell, move to `ExpenseManager` project folder (type `dir` and check if `requirements.txt` is present to ensure you are in correct repo).
3. type `pip install -r requirements.txt` to install dependencies for this project. Note: I didn't use virtual environment while making this app, so I had to manually edit dependencies( Another reason to not to avoid virtual env 😅 ), so if you bump into some module import error, try `pip install <missing_package>` and then re run the app. 
4. now type `cd app` to move to ExpenseManager/app folder.
5. now comment out both `app.secret_key = os.environ["APP_SECRET_KEY"]` and `_database = "postgres://ldhtwsrl...."` in MyApp.py with a text editor, then save and close so as to avoid interacting with heroku database instead of local db, test.db (sqlite).
6. type `set FLASK_APP=MyApp.py` (if you are using LINUX use `export` instead of `set`).
7. type `set FLASK_DEBUG=1`
8. type `flask run` to run the application on server.
9. Now your server is up and running. To view ExpenseManager page, go to `localhost:5000`.

#### If any error comes up while setting up, create an issue for the same.
