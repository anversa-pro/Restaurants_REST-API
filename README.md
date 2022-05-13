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
>       Gunicorn 20.1.0
>       flasgger==0.9.5
>       AWS Cloud Services

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
as good as on the repository route /Documentation/swagger.yaml:

## Usage
TBD

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
