# REST API Using Flask 
Small Flask Rest API for personal learning 

## Setup

### Installing Dependencies
- python3
- python3-pip
- python3-venv

### Setting up and running project

Then, on the project repository, do the following:
```shell
python3 -m venv venv
. venv/bin/activate
  
pip install -r requirements.txt

#optional: if you want to run the server on development mode export FLASK_ENV variable to 'development'
python -m flask run
```
Now you can access the API on localhost at: `http://localhost:5000/api`

For available endpoints, check the API Docs below

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

### Login

Login to the api (only Basic Auth allowed for now)

**URL**: `/api/login`

**Method**: `POST`

**Auth required** : NO

**Permissions required** : None

#### Success Response

**Code** : `200 OK`

**Content example**
```json
{
  "token" : "dfasdf1238ajds1sdafff8dsafjk1"
}
```

#### Notes

If you want to use an already created user with admin permission, you can use the following credentials in your Basic Auth:
```
username: admin
password: admin
```

### Products

#### GET Products

Get all available products endpoint

**URL**: `/api/products`

**Method**: `GET`

**Auth required** : NO

**Permissions required** : None

##### Sample Call
###### Success Response

For a request where the user wants the products be sorted in descending order by popularity, with pagination using page = 0 (offset), number of items per page = 3 and only getting the fields : name, price and stock, you can use the following URL.

**Request URL** : `/api/products?sort=-popularity&offset=0&limit=3&fields=name,price,stock`

**Code** : `200 OK`

**Header example**
```
Content-Type -> application/json
X-Total-Count -> 1000
Link -> <http://localhost:5000/api/products/?offset=0&limit=3>; rel="first"
Link -> <http://localhost:5000/api/products/?offset=325&limit=3>; rel="last"
Link -> <http://localhost:5000/api/products/?offset=1&limit=3>; rel="next"
Content-Length -> 187
Server -> Werkzeug/0.14.1 Python/3.7.1
Date -> Sun, 16 Dec 2018 20:55:29 GMT
```
**Content example**

```json
{
  "products": [
        {
            "name": "Island Oasis - Wildberry",
            "price": 374,
            "stock": 89
        },
        {
            "name": "Pork - Loin, Center Cut",
            "price": 407,
            "stock": 46
        },
        {
            "name": "Ostrich - Fan Fillet",
            "price": 180,
            "stock": 19
        }
    ]
}
```

**Sorting**

To sort the list by a field, use the sort parameter with a symbol as the first character. 
```
(+) -> sort in ascending order
(-) -> sort in descending order
```

**Pagination**

By default, the list of products is paginated with the following values:
```
offset = 0
limit = 20
```
You can specify them in the parameters as you wish. The number of items, as well as link to the prev, next, first and last page is specified in the headers.

**Filtering fields**

If the user only wants to receive certain fields from the request, they can be specified with a comma separated value.

Available fields:
```
name        -> name of the product
price       -> price of the product (in US dollars $)
stock       -> number of items available in the store
popularity  -> number of likes by users
search      -> text to search for in products name, it is surrounded by % symbols in db search query
```
