# online_shop
Online shop mini website

This is a Django project.

Configuration Setup

a. Install python2 and mysql server in your pc
b. create virtual env
c. Install lib from the requirements.txt
d. Then setup database credential and email credential in settings.py under Project folder
e. Then run the db migrations: python manage.py makemigrations
f. migrate the db: python manage.py migrate
g. can create the super user account: python manage.py createsuperuser
h. run the server: python manage.py runserver 8088
i. can configure Discount/ Customer Category settings via admin portal: localhost:8088/admin

