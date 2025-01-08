# This is a Set up for A Movie Reviews API
# SET-UP INSTRUCTIONS
# Create a virtual environment for your application, activate and add file extension to gitignore
# Install django 
# Create a django project using the command django-admin startproject project_name
# Next create the app/apps for the project using the command - python manage.py startapp app-name
# Add the installed apps to the settings.py file under the Installapps config
# Install the django rest_framework which will enable you build the apis using the command - pip install djangorestframework and add to the settings.py file
# Install the auth token provided by django_restframework to obtain token 
# MEsure that the Security middleware is installed as well contenttype to help handle security and auth for the api
# Configure the (SQL)databasee to use the Mysql engine for more roboost scalability

# AUTHENTICATION SETUP
# THE API makes use of the token based authentication framework called jwt (Json web token)
# This generates the token from an endpoint 'auth/token/' which the user can make use of for feature requests
# Also the authentication token can be generated from the traditional login endpoint, here we use the django predefined authentication module (django.contrib.auth) to authenticate and login user upon login the jwt token is generated and sent to the frontend for feature requests. 
# Test the Authentication visit the login or auth-token  endpoint and make the request providing your username and password

# Endpoint: api/auth/login/  (HTTP Method POST), 
# Request: { “email”:”test@gmail.com”, “password”:”123”}
# Response: {“message”: “User login successful”, "user_data": {“id”:id, “email”:”email”}, 'refresh_token':”token”, “access_token”:”token” } status_code is  200

# Endpoint: api/auth/token  (HTTP Method POST), 
# Request: { “email”:”email”, “password”:”123”}
# Response:Response: {“ refresh_token”:”token”, “access_token”:”token” } status_code is  200
