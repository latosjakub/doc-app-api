# **doc-app-api**
Documents app api source code.

 ## Starting GitHub Project
 1. Start by going to the github/repositores and click New button to creation page.
 2. Custimize your repository:
 * Repository name
 * Description
 * Choose this repo will be private or public
 * Add a README file
 * Add gitignore (python)
 * Choose a license (MIT)
 3. Next click create repository. This will create repository and take you to repo page.
 4. To copy repo to your local machine click a Code -> SSH and copy link for the repository.
 5. Lunch terminal in your project folder and type
 git clone <ssh url>
 This will download the entire repository


 ## Authenticate with Dockerhub
 1. Headover to dockerhub page
 2. Go to account settings -> security
 3. This allow us to create new access token when you authenticate to you github project with your dockerfile account
 4. Click new access token:
* gice a discription
!! Remember you are able to see token only once !
 5. To add a token to your repository go to repositpry page -> settings -> secreats and varables/actions
 6. Click New Repository Secret
    Give it a name(DOCKERHUB_TOKEN)
    Pass the dockerhub token
 7. Add your dockerfile username
     Click New Repository Secret
    Give it a name(DOCKERHUB_NAME)
    Pass the dockerhub username
This names are important bc we will be using them later in dockerfile

## Configure Docker
* Create a Dockerfile
* Lists steps for creating image:
 - Choose a base image(python)
 - Install dependencies
 - Setup users
* Setup Docker Compose(How our Docker image(s) should be used)
Define our "services
- name
- Port mapping
- Volume mappings

## Creating requirements.txt file
This is a list with all python requirements for this project.
Django >=4.1,<4.2 - This make supre tah the patch versioni s alvays up to date

## Adding Dockerfile
> Note: A dockerfile is simply a file that contains a list of instructions for Docker to build a Docker image. So you basically describe here all the dependencies that we need for our projext in out Dockerdile.

Idea
    add base file image
    add who maintaine dockerfile
    copy all nessesery files
    install dependencies
    create user
    add venv to path
    at the end of file switch to created user
1. Create a new file in our project's root directory called Dockerfile.


    * From python:3.10-alpine - the image that we're going to unherit our Docker file from. In this case we're going to create our Docker file from th e python 3.10 image. The one we're going to user is the 3.10 alpine 3.18. Alpine image it's a lightweight version of Docker.
    > Note: So with Docker we can basically build images on top of other imges. The benefit of this is that we can find an image tat has pretty much everything that we need for our project and then we can just add the customized bits that we need just for our specific product.
    * MAINTAINER Jakub Latos - this tells us who maintaining this Docker image.
    * ENV PYTHONUNBUFFERED 1 - it tells Python to run in unbuffered mode which is recommended when running Pythin within Docker containers.
    > This allow us to see the output of your application (e.g django logs) in real time. This also ensures that no partial outpu is held in a buffer somewhere and never written in case the python application crashes.
    *   copy all nessesery files
        First create new dir named app in our repo then in dockerfile user
        COPY ./requiremendts.txt /tmp/requirements.txt  (from to)
        COPY ./app /app -it copies from our local machine the /app folder to the /app followed that we've created on an image.
        > We first need to create dir named app in our local machine
        WORKDIR /app it switches to /app as the default directory. All command will run from this dir by default se we dant have to specify fyll path everytime.
        EXPOSE 8000 - expose port 8000 to our machine.
    *  Installing packages and delating unnesesery files.
        RUN python -m venv /py && \
            /py/bin/pip install --upgrade pip && \
            /py/bin/pip install -r /tmp/requirements.txt && \ - instaling things from requremendts.txt
            rm -rf /tmp && \ - we are removing temp dir bc we want our dockerimage to be lightweight as possible
            adduser \
                --disabled-password \- Why we disavle password?
                --no-create-home \ - we dont need home dir for user
                django-user - name of user

        Note: The reason why we do this is for security purposes. If we don't do this then the image will run our application using the root account which is not recommended because that means if somebody compromises our application they then have root access to the whole image. Whereas if we create a separate user just for our application then this limits the scope that an attacker would have in our documentation.

        ENV PATH="/py/bin:$PATH"

        USER django-user - switching to django-user
2. Creating .dockerignorefile
3. Docker-compose configuration
    Docker compose is a tool that allows us to run our Docker image easily form our project location.
    So it allows us to easily manage the different sevices that make up our project. So for example one sevice mioght be python application
    that we run. Another service might be the database.
    1. Create a new file in our project's root directory called docker-compose.yml:
    This is a yml file that contains the configuration for all of the services that make up our project.
    * version "3" - version of Docker compose that we're going to be writing our file for.
    *next we define services that make up our applicaton. Right now we only need one service for our Python Djano application
    services:
        app:
            build:
            context: .
    What this is we're going to have a srvice called app and the build seection of the configuration we're going to set the context to is "."
    which is our current directory that we're running docker-compose from.
        ports:
            - "8000:8000"
            volumes:
            - ./app:/app
            command: >
            sh -c "python manage.py runserver 0.0.0.0:8000"
            ports
        In this part we're going to map our project from port 8000 o our host to port 8000 on our image.
    volumes
    Volumes allows us to get updates what we make ti our oproject. It maps volume from our local machine here into our Docker containwe that will be runningour app.
    command
    This is a defaul command that will be executed at the start of the container. We might overwrite it when we start container
    using run parameter.
    python manage.py runserver 0.0.0.0:8000
    So this will run the django dev-server available on al the Ip addresses that run on the docker container. It's going to run on port 8000
    which is going to be mapped through the ports configuration to our local machine. So we can run our appllication and we can connect to it on port 8000 on our local machine.
# Creating Django project using the Docker configuration
    note WE used Docker comopse to run a command on our image that xontains the Django dependency and that will create
    the project diles that we need for our app. 
    1. Open terminal and navigate to the project's directory, then type 
    docker compose runn app sh -c "django-admin.py startproject app ."
    (remember you need have sudo privlages to run docker compose commnd)
    
    WE run commands useing docker compose by typing docker compose run and then the name of the service that we want to run command on. THis is if you have multipple services. Here we only have one service so we're just going to user our service called app. 
    When we user run we overwrite default commend described in docker-compose file. We type run sh -c so it runs a shell script. We pass in a command in speech marks.
     th e django-admin.py startapp app . is a django admin managment command we can user bc we installed django with requirements.txt file.  app is name of out project and "." it's telling we are starting project in currend workdir (which we specifided in dockerfile)

     What is Linting 
     * Tool to check code formatting
     * Highliights errors. typos, formating issues
    Whan we use linting tool is good practice to go from down to up with error meeseges bc when we go otherway we will change the lines of code in file so they want be accurate
    for linting i will user flake9 that checks python codebase for errors, styling issues and complexity.
    Note; It is very important to install Flake8 on the correct version on Python for your needs.Flake8 is tied to the version of
    Python on which it runs so it very important to use dedicated flake8 version for python that you use. 

    docker compose run --rm app sh -c "python manage.py test
    Testing 
    * Django test suite 
    *setup tests per django app
    * run tests through Docker compose 
     docker compose run --rm app sh -c "python manage.py test"


     Creating requirements.dev.txt is a file we create to additional step to install packages that will be usefull in development server but they are not 
     nessesery in actual server. We don't need lintig tool in our application server so we adding it in requirements.dev.txt We need to add additional step in 
     docker compose file 

     context:
     args:
        - DEV=true

     this will set our docker compose to the development mode so we can tell when we need additional packages and when we don't

     to docker file add 
     COPY ./requirements.dev.txt /tmp/requirements.dev.txt
     ARG DEV=false 

     > Note: we overwrite this behavior in our docker compose file so if we user docker run instead docker compose run we won't run our server in developer mode

     also we need to add if statment in docker file when we setup when we will install aditional packeges

     /py/bin/pip install -r /tmp/requirements.txt && \
     if [ $DEV="true" ]; \
            then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
            fi && \
    
    to configure flake8 we need to create file .flake8 inide app/ dir

    [flake8]
    exclude =
        migrations,
        __pycache__,
        manage.py,
        settings.py,
    docker compose run --rm app -sh -c "django-admin startproject app ."

    dot and the end of the command make django create project in this specified directory if we didnt user . at the end of the command django will create sub directory and than project inside this subdirectory. This subdir will be called as proiject name.
    
# Github Actions
IS automation tool similar to travis-CL, Gitlab CI/CD, Jenkins. It allows us to run jobs when code changes.
Common uses for github actions are:
- Deployment (we wont do this in this project)
- Code linting 
- Unit tests 
 
How its works

Trigger -> Job -> Results

Trigger
In this project we will user Push to Github as a trigger.
We can use different trigers if we want. They are listed in gihub dock https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows

Job 
Run unit test

Result 
Success/fail

Configuring github actions
    
Config file should be at .github/workflows/example.yml

we can name example.yml however we want as long as it and with .yml
In this file we will:
 - set trigger
 - add steps for runing testing and linting
 - set up dockerhub auth 
checks.yml
---
name: Checks - it si gonna apear in github actions

on: [push] - this is trigger

jobs:
    test-lint:
        name: Test and Lint
        runs-on: ubuntu-20.04 - this is operating system that we runs our jobs on 
        steps:
            - name: Login to Docker hub -this is name it is mainly for us to see what process are running rn
              uses docker/login-activation@v1 - this is premade action provided in github actions repository
              with:
                username: ${{ secrets.DOCKERHUB_USER }} - This creadencials are the one we added in project secreats 
                password: ${{ secrets.DOCKERHUB_TOKEN }}
            - name: Checkout
              uses: actions/checkout@v2
            - name: Test
              run: docker compose run --rm app sh -c "python manage.py test"
            - name: Linting
              run: docker compose run --rm app sh -c "flake8"

    
Note: ubuntu-20.04 have docker-compose preinstalled but diferent systems can dont have it and than we need to add some steps to download this package

# Testing 
    Django test framweork

    Django test framework is build on top  of a unittest library. The most important features we will user are:
    Test Client -fummy web browser
    Simulate authentication 
    Temporary database 
    Django Rest framweork adds d=features 
    API Test Client - Client createt for testing apis.

# Where to put tests
    We can store our test in few different ways:
    - Placeholder test.py file added to each app
    - Create tests/ subdirectory to split up tests
    When we create subdir we need to remember to create __init__.py file. Also every module need to starts with "test_".

    Test Classes 
    SimpleTestCase - This dont have any database integration. Whe should user this class when we run test that dont need database. Benefit of using this class to tests is time because we dont have to create and clear database our test are simply faster.
    TestCase -This class have database integration. Use it to database related test. Write from database ect.

# Creating First test
    TDD Test Driven Development 
    First create a test and then create a funcionality for this test.

    It is very important to use test.py file or test subdir
    function 



    BRBBRBRBRBRBRBRBRBBRBR
# Mocking
    Mocking is chenging or overwritting behavion of dependencies for purpose of your tests.
    Benefits of mocking
    - This prevent us for unintended site effects.
    -isolate code being tested
    - avoiding relying on external services 
    - makes tests predictible and consistent
    -  Avoiding unintendent consequences:
            * Accidently sending emails.
            * Overloading external services 
    - Speads up tests

# Mocking Database 
    Use unittest.mock
        - Magicmock/mock - replace real objects
        - Patch Overrides code for test 

# Testing web request 


# Database architecture overwiev.

# Volumes 
    Volumes allow us to store persistent data using docker compose. This maps dir inside our container to our local machine.

    VOlumes are define at the end of docker compose configuration
        db:
            image: postgres:13-alpine
            volumes:
                -dev-db-data:/path/to/database/in/container  - mapping volume in container
    
    volumes:
        dev-db-data:   - this is volumes on our local machine
        dev-static--data:

    
# Adding database service

    Database service is defined in docker compose file as a servicce. 

    so we update docker compose file with code below
        environment:
            - DB_HOST=db
            - DB_NAME=devdb
            - DB_USER=postgresqluser
            - DB_PASSWORD=changeme 
        depends_on:
            - db

    db:
            image: postgres:13-alpine
            volumes:
                -dev-db-data:/var/lib/postgresql/data
            environment:
                - POSTGRES_DB=devdb
                - POSTGRES_USER=postgresuser
                - POSTGRES_PASSWORD=changeme

    
    volumes:
        dev-db-data:   - this is volumes on our local machine

    NOTE if you run docker compose up after this it will create config in volumes so  if later you change password here it wont connect to the database 
    if you done this use

    docker compose down --volumes
    docker-compose up



# Connecting djnago to database:
    What django needs:
    Engine (type of database)
    Hostname(IP or domain name for database)
    Port
    Database name
    Username
    Password

    In django settings file we define connection

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': os.environ.get('DB_HOST'),
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD' os.environ.get('DB_PASS'),
        }    }
    
    This will pull environment var from docker. This is good practice to pull everything from env vars
    because if we want to change them. We only change this in one place in code.

    


# Wait FOR Db Command
We need to make sure that db start before our app bc app may crash if db wont be ready. For prevent thios from happening 
we will make wait for db command tah will make our app wait for database.



# Creating a core app and setting up models.py 

Preparing the environment
The first thing we're going to do is we're going to create a core app which will hold all of the central code that is important to the rest of the sub apps. It's going to create anything that is shared between other apps like migrations, database. 

1 In the terminal lunch docker compose run app -rm sh -c "python manage.py startapp core"

2 Delete unnessesery files like tests.py (we will make test subdir), views.py(core app wont serve any web views)

3 Now we crete a tests subdor insiede core app folder and create __init__.py fille.
Note:     When the Python interpreter encounters a directory containing an __init__.py file, it recognizes that dir as package.The __init__.py file is executed as the package's initialization code when the package is imported.

4 Add core app inside settings.py INSTALED_APPS.


Write tests for wait_for_db command.

1. Firdt, go into core/tests/tests_commands.py

We wi'll testing  our functions for tetesing if databse is ready to use.
2. Inside tests_commands.py add imports

    from unittest.mock import patch

    from psycopg2 import OperationalError as PSycopg2Error
    we are using as bc both imports have the same name
    from django.db.utils import OperationalError
    Two imports above are for simulate errors that can accur during connecting to db

    from django.core.managment import call_command
    
    from django.test import SimpleTestCase

@patch('core.managment.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True
        

        call_command('wait_for_db')

        patched_check.assert_called_once_with(datavases=['default])

patch added before class will apply on every method of class

 return value let us set this to configure the value returned by calling the mock. The default retrun valuue is a mock object and you can configure it. More at https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.return_value

 class SimpleTestCase it simple test class that we use when we dont need test database for our tests. More at 
 https://docs.djangoproject.com/en/3.2/topics/testing/tools/#django.test.SimpleTestCase

    @patch('time.sleep')
    def test_wait_for_db_ready(self, patched_sleep, patched_check):
        """Test waiting for database wen getting Operational Error."""
        patched_check.side_effect = [Psycopg2Error] * 2 =\
        [OperationalError] * 3 + [True]
        

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(datavases=['default])

Remember using multiple patch you need to set correct order. This go "inside out" so time.sleep will be passed as a first argumend and check as a secound.

Creating custom django managment command

1. Create nessesery folders core/mangement/commands and create file wait_for_db.py in management and commands folder create file
__init__.py otherwise commands wont work.

2. Then add inmports
    import time 
    from psycopg2 import OperationalError as Psycopg2Error
    from django.core.managment.base import BaseCommand
    from django.db import OperationalError

3. Then create class Command thath inherets from BaseCommand

4. Add handle methon that takes *argsn **options

    def handle(self, *args, **options):
        """Enrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database unavalible, waiting 1 sevond...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!))
        aaaaaaaaaaaaaaaaaaaaaa