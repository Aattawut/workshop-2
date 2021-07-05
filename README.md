# Workshop-2

## POSTMAN Link 
- [link Postman](https://www.postman.com/collections/583523dda916141cfa6a)
- `import postman env from /postman-env/env-workshop2.postman_environment.json`

## Project setup

- `cd workshop1` 
- `python3 -m venv workshop2`
- `source workshop2/bin/activate`
- `pip install -r requirements.txt`

## Start Develop
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver 0.0.0.0:8000`
## init data
- `python manage.py loaddata cactusshopdb/cactusshop.json`
 
