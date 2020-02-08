# Thai Tran

### Installation

This program requires Python 3.6 or above to run.

1. Some requirements:

    Install pip, if you don't already have:

    ```commandline
    easy_install pip
    ```

    Install virtualenv if you don't already have

    ```commandline
    pip3 install virtualenv
    ```

 2. Choose a folder to install. Create and activate new virtualenv.

    Create a virtual environment to isolate our package dependencies locally
    ```
    python3 -m venv paranuara_env
    source paranuara_env/bin/activate
    ```

 3. Install Paranuara

    ```commandline
    pip install -r requirements
    ```

 4. Run these commands to instantiate new paranuara application:

    ```commandline
    python manage.py migrate
    python manage.py loaddata
    python manage.py runserver
    ```
Then navigate to http://localhost:8000

### Usage

* To wipe database and import new JSON data use following commands:

    ```commandline
    python manage.py flush --noinput
    python manage.py loaddata --path /this_is/my_path
    ```
    Where /this_is/my_path is path to people.json and companies.json

* To run tests:

    ```commandline
    python manage.py test paranuara.test.tests
    ```

## Rest API endpoints:

1. http://localhost:8000/companies/1

    Given a company (index), returns all its employees.
    Where `1` is index of the company as specified in source data.

2. http://localhost:8000/peoples/friends_in_common/?ids=998,999

    Given 2 people, provides their information (Name, Age, Address, phone) and
    the list of their friends in common which have brown eye and are still alive.
    Where `998` and `999` are indexes of people as specified in source data.

3. http://localhost:8000/peoples/2

    Given 1 person (index), provides a list of fruits and vegetables they like. This endpoint
    respects this interface for the output:
    ```json
    {"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}
    ```