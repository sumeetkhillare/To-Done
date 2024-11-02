# Quick Start

 * [Download](https://www.python.org/downloads/release/python-390/) and install Python 3.8.0 or higher
 * [Install](https://docs.djangoproject.com/en/4.2/topics/install/) Django 4.2
 * Clone the repository
    ```bash
    $ git clone git@github.com:se-zeus/To-Done.git
    ```
* Change directory
    ```bash
    $ cd To-Done
    ```
* Install necessary libraries
    ```bash
    $ pip install -r requirements.txt
    ```
 * Run migrations
    ```bash
    $ python manage.py makemigrations
    ```
* Migrate the DB
    ```bash
    $ python manage.py migrate
    ```
 * Start the app
    ```bash
    $ python manage.py runserver 8080
    ```
 * Point your browser at http://localhost:8080 and explore the app