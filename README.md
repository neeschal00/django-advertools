# django-advertools
A wrapper for the advertools library to show different functionalities in django

This Project utilizies the library named **Advertools** https://advertools.readthedocs.io/en/master/ created by eliasdabbas (https://github.com/eliasdabbas). The library consists of different helper functionalities ranging from Search Engine Optimization (SEO), Search Engine Marketing (SEM), Text Analysis. The workaround with pandas to view data makes it easily analyzable and viewable based on attributes and fields associated with the functionality.

## Tools and Technologies used
- Python
- Django
- ChartJS
- Celery 
- Pandas 
- Y Data Profiling
- Data Tables Jquery
- Select2 js lib


## What does this project Do:

This django wrapper utilizes the above mentioned tools and technologies in order to create and implement those feature with user associated input as well as preprocessing some inputs for making it appropriate to pass as a parameter for those methods. The project utilizes Data Tables library of jquery to view pandas tables (i.e. converted to html table) in template in paginated format with additional feature to search the table, view only selected column as well as exporting the table in csv, excel, pdf, etc. The ChartJS library is used to create charts for few feature to visually represent data to show an overview as well as distinction for few of the dataset. The forms are organzied and prioritized based on the required and optional fields in the templates and django forms.


## How to run this project

- Setup venv, activate and install packages from requirements.txt
```
python -m venv venv
```
```
venv\Scripts\activate # for windows
venv\bin\activate # for linux
```
```
pip install -r requirements.txt
```

- Migrate the database changes
```
python manage.py migrate
```

- Run django server
```
python manage.py runserver
```

- Run Celery
```
celery -A django_advertools worker -l info -P solo #p solo for pool solo arg in win for execution
```

Optional Arguments if celery is receiving the tasks but not executing
```
--without-gossip --without-mingle --without-heartbeat -Ofair
```
