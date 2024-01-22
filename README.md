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

To run Coverage:
coverage run python manage.py test

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
Now create a resource -> webapp
Select docker container and other info and select free plan

Click next to docker and select private container registry

Private container registry settings settings
SERVER URL : https://ghcr.io
USERNAME: your username
PASSWORD: your PAT from github (create one at https://github.com/settings/tokens)
FULL IMAGE NAME AND TAg : ghcr.io/<your username>/publish-packages/hotrocksv2:latest

Once ths is created you should be able to view your web app.

Nnow turn on the continous deployment:
Deployment -> Deployment Center contains the container settings
Curn on continuous deployment and save

Continouous Deployment creates a webhook URL we will use when the docker push gets triggered by the github push.

Copy the Webhook URL.  Go to Github -> Your Repo -> Settings - > Webhooks and create a new webhook.  Use the URL copied, the rest of the settings you can leave as default.

Now back in azure, in the webapp control panel go to Settings->Configuration and add all of tge enviornment variables in your local .env file to the Application Settings section. Dont forget to save it.

