# Piecy

## Introduction
Piecy is a web application designed to efficiently manage a car spares business or any business with similar setup and workflow.

## Requirements  
### Skills
- Familiarity with Linux systems
- Basic knowledge of Django ecosystem

### Setup and software
- Anything that runs Python and Django, with internet connectivity. We are using Rocky Linux.
- Python, git and code or text editor.

## Testing/Development
- Clone the repo with git or download and extract the zip.  
  ```git clone https://github.com/Julinium/piecy.git```  
  ```cd piecy```  

- Create a python virtual environment, if not already done, and source from it.  
  ```python -m venv .venv```  
  ```source .venv/bin/activate```  

- Install dependencies from requirements.txt.  
  ```pip install -r requirements.txt```  

- Copy .env.example to .env and change values as needed.  
  ```cp .env.example .env```  

- Tune piecy/settings.py accordingly.  
- Make migrations and migrate.  
  ```python manage.py makemigrations```  
  ```python manage.py migrate```  

- Create a superuser (needed to access admin site).  
  ```python manage.py createsuperuser```  

- Run the server for test.  
  ```python manage.py runserver```  
  If accessing the server from the network, make sure to add its ip address to ALLOWED_HOSTS and allow port 8000 in firewall, if enabled.

## Production
- Setup a WSGI and a webserver.
- Setup a firewall.
- ...