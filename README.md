# hotrocksv2

Asphalt Company Management Software

Apps:
crewcal - displays calendar of jobs
report - incident reporting

# Ininitial Setup
This has been written on python 3.11.

First clone the repository:
git clone https://github.com/agshadow/hotrocks

set up virtual environment:
python -m venv venv

install packages from requirements.
pip install -r requirement.txt

how to run in debug mode:
python manage.py runserver

should be running on http://localhost:8000

# Testing

to run unit tests:
python manage.py test

to run individual test 
python manage.py test crewcal.tests.TestHome.test_should_be_able_render_cal_page

to run individual or groups of tests using Django Awl module:
python manage.py test =cal_page

# To update requirements.txt with new modules
pip freeze > requirements.txt


# SET UP Postgres

Create Elephant DB account. Please note my Elephand DB was running 
postgres 11.19 and Django 4.2 requires version 12.
I downgraded to Django 4.1 for this
Create new database (free) instance
Create local .env file with the following:

---------------------------------
DATABASE_NAME=<postgresql_username>
DATABASE_USER=<postgresql_username>
DATABASE_PASSWORD=<postgresql_password>
DATABASE_HOST=<postgresql_server>
DATABASE_PORT=5432
----------------------------------

You can populate the database with the scripts/populate_cal_db.py by pasting
it into a django shell


# Set Up azure
now create a resource - webapp
select docker containerand other info
and select free plan

click next to docker
select private container registry

in docker settings
SERVER URL : https://ghcr.io
USERNAME: your username
PASSWORD: your PAT from github (from https://github.com/settings/tokens)
FULL IMAGE NAME AND TAg : ghcr.io/<your username>/publish-packages/hotrocksv2:latest

once ths is created you should be able to view your web app.

now turn on the continous deployment:
Deployment -> deployment center contains the container settings
turn on continuous deployment and save

this continouous deployment creates a webhook resource which will fire which will fire each time we push a container.  

copy the web hook and add it to your github -> repo -> settings - > webhooks

now still in the webapp control panel go to settings->Configuration and add enviornment variables as per the local .env file, to the Application Settings section. Dont forget to save it.