# ExpenseManager
A web app for expense manager made using Flask (a python microframework).
Made for CSI, NSIT event. 

## Key Features:
1. Data visualization for user
2. Set and add budget for a given month.
3. Set expenditure daily or on a monthly basis.
4. Use of python libraries and jinja to avoid Javascript and Jquery completely.
5. Login authentication. (created using python decorators)
6. Database access only for admin.

# Local Development Setup

The instructions on this page will guide you in setting up a local development
environment in Windows OS.

1. Fork this repo, and then clone your forked copy:
Open git terminal(Git bash in windows), and clone your forked repo i.e. `git clone https://github.com/<your_username>/ExpenseManager.git` in the directory you want.
2. Now using cmd or powershell, move to `ExpenseManager` project folder (type `dir` and check if `requirements.txt` is present to ensure you are in correct repo).
3. type `pip install -r requirements.txt` to install dependencies for this project. Note: I didn't use virtual environment while making this app, so I had to manually edit dependencies( Another reason to not to avoid virtual env 😅 ), so if you bump into some module import error, try `pip install <missing_package>` and then re run the app. 
4. now type `cd app` to move to ExpenseManager/app folder.
5. type `set FLASK_APP=MyApp.py` (if you are using LINUX use `export` instead of `set`).
6. type `set FLASK_DEBUG=1`
7. type `flask run` to run the application on server.
8. Now your server is up and running. To view ExpenseManager page, go to `localhost:5000`.

# To Do:

1. Deploy app on heroku (which I tried, but I need to shift to postgresql from sqlite which is creating errors which are yet to be solved 😫, need some time). (Sorry for inconvenience caused) 
2. Use Bokeh ✨ instead of pygal for data visualization.
3. Plotting of purchase location of a user in a map.
4. Add more features to the app like,providing a option to add a new category, use Wordnet to automatically add expenditure of a user in one of the pre-defined categories by comments.
5. Comparision of a user with average users in terms of budget and expenditure.
6. Add relevant in home tab in the dashboard.
