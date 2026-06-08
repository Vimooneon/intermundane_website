# Intermundane website

Developed using python (version 3.13.1) and django library (version  6.0.6)


# Steps for localhost testing:

- Cloning repository:
```
git clone <repository-url>

cd intermundane_website
```
- Creating virual environment:
```
python -m venv venv

.\venv\Scripts\activate
```
- Installing dependencies
```
pip install django django-parler
```
- Compiling translations

requires GNU gettext tools (https://mlocati.github.io/articles/gettext-iconv-windows.html)
```
django-admin compilemessages
```
- Creating database
```
python manage.py migrate
```
- Creating admin user and access levels
```
python manage.py shell

#importing models

from intermundane.models import User, AccessLevel

#at least 1st access level must exist to create accounts

AccessLevel.objects.create(id=1, name="Guest", level=0)

AccessLevel.objects.create(id=2, name="Registered user", level=1)

#creating account with admin priviledges

usr = User.objects.create(id=1, username="admin")

usr.set_password("secret")

usr.is_staff=True

usr.is_superuser=True

usr.save()
```
- Running local server
```
python manage.py runserver
```
by default local server runs on http://127.0.0.1:8000/

further database editing can be done by visiting http://127.0.0.1:8000/admin and logging in as admin user

# Project folders structure
intermundane/

   migrations/ - database migrations
    
   templates/ - HTML templates
    
   views/ - django views
    
locale/ - Translation files

mysite/ - Site hosting settings

static/ - Static files (CSS, JavaScript)

# Accessing website

Website is hosted with the help of www.pythonanywhere.com

website is hosted on: https://intermundane.pythonanywhere.com/
