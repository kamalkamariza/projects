# A description for this project

Frameworks
1. Python >= 3.9
2. Django >= 3.2

Steps to run the project
1. create a virtual environment using the minimum python version with `python3 -m venv env`
2. activate `env` with `source env/bin/activate`
3. install packages if haven't with `pip install -r requirements.txt`
4. run the django server with `python manage.py runserver`
5. Homepage url `` will be the upload_csv view where user can upload a csv into db
6. `display-rankings/` will show all the teams and their ranks
7. `match-list/` will shows the records of all their matches
8. CTRL-C to quit the server