# Restaurants REST API

>   **This project is an HTTP server REST API implementation**

## Objectives: 
*  Creating a registration service that receives an email and a password.
*   Allowing login into the server with an email and a password.
*   Allowing logged in users to do CRUD operations into the table.

## Table of Content
* [Architecture](#architecture)
* [Technology Stack ](#technology-stack)
* [Environment](#environment)
* [Installation](#installation)
* [File Descriptions](#file-descriptions)
* [Usage](#usage)
* [Examples of use](#examples-of-use)
* [Bugs](#bugs)
* [Author](#author)
* [License](#license)

## Architecture
TBD

## Technology Stack
>       Python 3.8.10   
>       Flask 2.1.2
>       AWS Cloud Services
>           RDS
>           EC2
>       MySQL Server 8.0
>       MySQL Client 2.1.0
>       SQLALchemy 1.4.36
>       Gunicorn 20.1.0
>       flasgger 0.9.5
>       bcrypt 3.2.2
>       pyJWT 1.4.2

## Environment
This project was developed on Ubuntu 20.22 LTS using python3 (version 3.8.10)
In the requirements.txt file, you'll find all specifications.

## Installation
* Clone this repository
>       $   git clone "https://github.com/anversa-pro/restaurants-rest-api"
* Access 'restaurants-rest-api' directory: 
>       $   cd restaurants-rest-api
* As good practice I suggest you create a virtual environment, e.g.
>       $   python3 -m venv myvenv
* Activate the new environment
>       $   source myevn/bin/activate
* Install the requirements
>       $   pip install -r requirements.txt
* Run the program
>       $   python3 app.py
* Now you are running the API and available to create requests locally and test functionality.
* Further you can test the program with POSTMAN, in the Documentation directory, you'll find a collection 
of tests of each endpoint.
* When you are done, terminate the app process with CTRL+c and deactivate the venv.
>       $   deactivate

## File Descriptions
The API documentation is available on: Restaurant REST API Documentation 
as good as on the repository route /Documentation/ also you can access to 
an interface with yor localhost:8000/apidocs/

app.py - contains the entry point of the API.
documentation/ directory contains files used for document endpoints of this project:

    authentication.yml
    create_restaurant.yml
    create_user.yml
    delete_restaurant.yml
    get_cities.yml
    get_city_by_id.yml
    get_countries.yml
    get_country_by_id.yml
    get_random.yml
    get_restaurant_by_id.yml
    get_restaurants.yml
    get_user.yml
    get_user_restaurants.yml
    update_restaurant.yml

models/ directory contains classes used for this project:

    restaurant
    city
    country
    user

routes/ directory contains endpoints used for this project:

    restaurant
    city
    country
    user
    random
security/ directory contains functions used to encrypt and decrypt tokens to identify users for this project:

    security

validators/ directory contains methods used to check requests parameters

    password
    user
    validator

## Usage
The repo contains the access to the AWS RDS  with prefilled data, 
and a Gunicorn server over EC2 is available to test the API. 
The access to that connection is temporary, in case it is no longer available, 
you can find a data file in the repo to build it locally or with your preferred provider.

Three ways to test the API:

### Postman
Load the collection in the path _______ into your postman count.

### API URL powered by flasgger
Open the url: _______:8000/apidocs in your browser

### Console
Open a console to use the method cURL method.

## Examples of use
TBD

## Bugs
No known bugs at this time.

### Author
Angela Vergara | 
[LinkedIn](https://www.linkedin.com/in/angela-vergara-salamanca/?locale=en_US) | 
[Github](https://github.com/anversa-pro) |

## License
Public Domain. No copy write protection.
