# This is a Set up for A Movie Reviews API

# SET-UP INSTRUCTIONS
####  Create a virtual environment for your application, activate and add file extension to gitignore
####  Install django 
####  Create a django project using the command django-admin startproject project_name
####  Next create the app/apps for the project using the command - python manage.py startapp app-name
####  Add the installed apps to the settings.py file under the Installapps config
####  Install the django rest_framework which will enable you build the apis using the command - pip install djangorestframework and add to the settings.py file
####  Install the auth token provided by django_restframework to obtain token 
####  MEsure that the Security middleware is installed as well contenttype to help handle security and auth for the api
####  Configure the (SQL)databasee to use the Mysql engine for more roboost scalability

# INTEGRATION OF THIRD-PART API 
#### A third part api (OMDBAPI) is intergrated to fetch the movie details particularly the title and store in the movies tables
#### The operation involves fetching the movie through the api along with queried params.
#### A custom management command is setup to run/trigger the handle() to excute in other to perform the action before running the server. 

# AUTHENTICATION SETUP
#### THE API makes use of the token based authentication framework called jwt (Json web token)
#### This generates the token from an endpoint 'auth/token/' which the user can make use of for feature requests
#### Also the authentication token can be generated from the traditional login endpoint, here we use the django predefined authentication module (django.contrib.auth) to authenticate and login user upon login the jwt token is generated and sent to the frontend for feature requests. 
#### Test the Authentication visit the login or auth-token  endpoint and make the request providing your username and password

#### Endpoint: http://127.0.0.1:8000/api/auth/login/  (HTTP Method POST)

####  Endpoint: http://127.0.0.1:8000/api/auth/token  (HTTP Method POST)

# Users Management CRUD Operations
#### This manages the Users data and ensure that users can create read update and delete their own data. The following endpoints are available for the user to perform various action along with the sample request and response data. 
#### First the User regisration endpoint to this the path the user to visit once they need to create an account

### Register Account
#### Endpoint:  http://127.0.0.1:8000/api/auth/register/ (HTTP METHOD POST)


#### Read User Details
### Request: http://127.0.0.1:8000/api/user/1/ (HTTP Method GET) 


#### Update User Details
### Request Endpoint: http://127.0.0.1:8000/api/user/1/update/ (HTTP Method PUT OR PATCH) 


#### Delete User Details
### Request Endpoint: http://127.0.0.1:8000/api/user/1/update/ (HTTP Method PUT OR PATCH) 


# Movie Reviews Management CRUD Operation
#### The movie review management basic CRUD endpoints as well as searching and filtering endpoints. The review table has a one-to-many relationship with the Movie and User table. This data relation ensures that multiple users can leave a review for a single movie and vice versa. To implement this CRUD operaion django rest_framework ModelViewset was use to implement the straight operation.
#### For the creation for movie reviews the user can add a review but  can not submit multiple reviews for the same movie.
#### To create the review the request data passed in the body of the request includes the movie_title which is a foreign key to the movie table. Below is the sample request for each of the CRUD operation and the data returned. Also you can perform a filter to retrieve reviews by specific movie_title from a dedicated endpoint which was created for it. The permission where implemented to restrict users to only update or delete their reviews as well as update or delete their user account.
#### The following permissions  where implemented:
#### IsAuthenticated
####  CustomPermission (which denotes a custom permission to check that the user has an object level permission thus can only update or delete their reviews).

#### Create review Endpoint:
#### Endpoint:  http://127.0.0.1:8000/api/reviews/ (HTTP METHOD POST)


#### View a specific Reviews:
#### Endpoint Request: http://127.0.0.1:8000/api/reviews/2/  - HTTP Method: GET


#### Show All reviews:
#### Endpoint Request: http://127.0.0.1:8000/api/reviews - HTTP Method: GET

#### Update OR Partially Update Review Endpoint:
####  Endpoint Request: http://127.0.0.1:8000/api/reviews/2/ - HTTP Method: PUT/PATCH

#### Delete Review Endpoint:
####  Endpoint Request: http://127.0.0.1:8000/api/reviews/2/ - HTTP Method: DELETE


#### Search movie Review by Movie Title or rating and ordering: 
#### Endpoint Request: http://127.0.0.1:8000/api/reviews/?search=IntoBandlands&ordering=created_at  HTTP Method: GET

#### Dedicated Endpoint Filter Review by Movie Title:
#### Endpoint Request: http://127.0.0.1:8000/api/reviews/movies/?title=  HTTP Method: GET

#### Filter Review by rating returning reviews based on minimum and maximum rating:
#### Endpoint Request: http://127.0.0.1:8000/api/reviews/movie_title=&min_rating=4&max_rating=  HTTP Method: GET


