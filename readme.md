# REST API Using Flask 
Small Flask Rest API for personal learning 

## Setup

### Installing Dependencies
- python3
- python3-pip
- python3-venv

Then, on the project repository, do the following:
```
python3 -m venv venv
. venv/bin/activate
  
pip install -r requirements.txt
  
export FLASK_APP=api
python -m flask run
```
Now you can access the API on localhost at: `http://localhost:5000/api`

## API Documentation

### Register

Sign up a new user to the api

**URL**: `/api/register`

**Method**: `POST`

**Auth required** : NO

**Permissions required** : None

#### Sample Call
If you want to register a user with username `snacks` and password `snacks`, make the request body like the following:
```json
{
  "username" : "snacks",
  "password" : "snacks"
}
```

#### Success Response

**Code** : `201 OK`

**Content example**
```json
{
  "message" : "user created"
}
```
