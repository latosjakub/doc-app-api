# **DOC-APP-API**
# Description

This application, built on Django and Django Rest Framework, functions as a documents platform, allowing users to quickly add, delete, and update posts. Treated as a personal notebook for exploring Django and DRF, the README outlines the entire project creation process and thoroughly explains its features. The app aims to improve information flow within organizations, promoting better organization and management.

Technologies
* Docker
* Python
* Django
* Django Rest Framework
* Postgresql

Features
* User Authentication
* Managing users by Django Admin Page
* Browseable API (using swagger)
* Add, delete and update Posts
* Tagging posts
* Uploading Files




 # Starting GitHub Project
1. Begin by visiting the GitHub repositories and selecting the "New" button to initiate the creation page.
2. Personalize your repository settings, inluding:
    * Repository name
    * Description
    * Privacy setting
    * Addition of a README file
    * Inclusion of a Python .gitignore file
    * Selection of a licence (MIT)
3. Proceed to create the repository by clicking the "Create repository" button, which will generate the repository and redirect you to its page.
4. To clone the repository to your local machine, click on "Code", select SSH option, and copy the provided link.
5. Open the terminal in your project folder and enter the command:

    `git clone <ssh url>`


 ## Authenticate with Dockerhub
1. Navigate to the Docker Hub page.

2. Access your account settings and proceed to the security section.

> This step allows the creation of a new access token for authentication in your GitHub project using your Docker Hub account.

3. Select the option to generate a new access token.

4. To incorporate the token into your repository, visit the repository page, then go to settings and secrets or variables/actions.

5. Create a new repository secret:
   * Provide a name (e.g., DOCKERHUB_TOKEN)
   * Enter the Docker Hub token.

6. Include your Dockerfile username:
    Create another repository secret.
    * Name it (e.g., DOCKERHUB_NAME).
    * Enter your Docker Hub username.

> These names are crucial as they will be utilized later in the Dockerfile.

# Configure Docker
1. Create a Dockerfile.
2. Steps for image creation:
    * Select a foundational image (e.g., Python).
    * Install necessary dependencies.
    * Configure user settings.


    * Establish Docker Compose specifications for utilizing Docker image(s):
        * Define services.
            * Specify service names.
            * Map ports.
            * Define volume mappings.



# Adding Dockerfile
> A Dockerfile is essentially a document containing a set of instructions for Docker to construct a Docker image. In essence, it outlines all the dependencies required for our project within the Dockerfile.

### 0. Steps

* Include the base file image.
* Specify the maintainer of the Dockerfile.
* Copy all necessary files.
* Install dependencies.
* Create a user.
* Add the virtual environment (venv) to the path.
* Towards the end of the file, switch to the created user

### 1 .Create a new file in our project's root directory called Dockerfile.


From python:3.10-alpine`


> Docker allows us to build images by starting with existing ones. This is handy because we can find an image that already has most of what we need and then just add the specific things our project requires.


`MAINTAINER Jakub Latos` - this tells us who maintaining this Docker image.

`ENV PYTHONUNBUFFERED 1` it tells Python to run in unbuffered mode which is recommended when running Pythin within Docker containers.
> This allow us to see the output of your application (e.g django logs) in real time. This also ensures that no partial outpu is held in a buffer somewhere and never written in case the python application crashes.

* copy all nessesery files. First create new dir named app in our repo then in dockerfile.

`COPY ./requiremendts.txt /tmp/requirements.txt`
`COPY ./app /app`


`WORKDIR /app`
> It sets the default directory to /app. As a result, all commands will automatically run from this directory by default, eliminating the need to specify the full path each time.


`EXPOSE 8000`  expose port 8000 to our machine.
*  Installing packages and delating unnesesery files and creating user.

`RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user `

The reason why we switch to django user is for security purposes. If we don't do this then the image will run our application using the root account which is not recommended because that means if somebody compromises our application they then have root access to the whole image. Whereas if we create a separate user just for our application then this limits the scope that an attacker would have in our documentation.

`ENV PATH="/py/bin:$PATH"`

`USER django-user` - switching to django-user

### 2. Docker-compose configuration
>Docker Compose helps us run our Docker image from our project folder, making it easy to handle different project services. For example, we might have a Python application or a database as separate services.


1. Create a new file in our project's root directory called `docker-compose.yml`
This is a yml file that contains the configuration for all of the services that make up our project.
* version "3" - version of Docker compose that we're going to be writing our file for.


* next we define services that make up our applicaton. Right now we only need one service for our Python Djano application
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

User model common issues
Running migrations before setting custom model
-set custom model first
-typos in config
Design Custom user model
*email(EmailDield)
*name(CharField)
*is_active(BooleanField)
*is_staff(BooleanField)
*is_acco(BoleanField)
*is_it(BooleanField)

User model mangaer - is used to manage objects it allow us to apply custom logic for creating objects like hash passwords

# Creating user model tests
Testing creating new user when email is successful

1. Create new file app/core/tests/test_model.py

WE'll be testing if our helper fucntion create_new_user is able to create user as we wanted.

2. Add imports TestCase class and get_user_model:

    from django.test import TestCase
    from django.contrib.auth import get_user_model

NOte: get_user_model helper function is provided by django to get default user model that is configured in our project.

3. Create test class called ModelTests. We'll creeate tests for all our models. Next create method called test_create_user_with_email_successful.

4. Now we creating test where we pass email and password for creating user and veryf is function works correctly. We'll do that by checking if user has been created and compare if email and password are the same as we gave to that function.

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=passowrd,
        )

        self.asserEqual(user.email, email)
        self.assertTrue(user.check_password(password))

 So we get user model  using get_user_model than we use.objects which is reference to our manager thath we gonna create adn we calling create_user method onthe UserModel.

We can't check the password the same way like we did checking an email. This is because the password is encrypted so we can only check it using the check_password function on our user model.

Creating user model
 first we add imports
 from django.sb import models
 from django.controb.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
 )

 Then we create User class inherate AbstractBaseUser which provide funcionsality for auth system and Permissionsmixin.

 next we define fields
 email(unique),name,is_active(def.true),is_staff(def.false).

 then we replace default field for authentication by USERNAME_FIELD = 'email' after that we assign UserManager which we will create in next step. objectss = UserManager()


 Creating user manager

 1. Create Class UserManager inherate from BaseUserManager.

 2. In User manager we create method called create_user.


    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

setting password to None give use an optiont o create non usable user which can be usefull for testing.

**extra_fields let us provide keyward arguments. This is helpful when we adding new fields to user bc we dont need to adding them in create_user method. self.model is the same as defining new user bc this is manager which is user assigned to.

we are using function set_password bc it hash the password. user.save(using=self._db) is for support multiple databases. Ofc in this project we will only using one.

is settings of the project we need to define custom user model. at the bottom of the file add AUTH_USER_MODEL = 'core.User'

after that we can make migrations

warning If you see arror inconsistentMigrationsHistory you need to clear your volume to do that docker compose ls to see volumes and then docker volume rm name of volume

Testing if the email for user is normalized

Now that we have our create_user function we can add new feature to the function to normalize email address that user signup with. Secound part of email should be case-insensitive so we are going to make that part all lowercase.

1. Inside Model Test calss in test_models.py add new function called test_new_user_email_normalized.

2. Inside this function create an 2 dem list with email with mixed upper and lower case domain expencions on first possition and lower case on secound.

3. Below, let's create loop and within the loop create user usind list of email and use assertion to see if emails are normalized correctly.



so whole test function should looks like this.

    def test_new_user_email_normalized(self):
    """Test the email for new user is normalized."""
    sample_emails = [
        ['test1@EXAMPLE.COM', 'test1@example.com'],
        ['Test2@EXample.com', 'Test2@example.com'],
    ]
    user = get_user_model().objects.create_user(email, 'testpass123')

    self.assertEqual(user.email, email.lower())

5. Save this test file and let's head to our terminal and let's run our unit test.

Now add normalization with changind email  field for
    user = self.model(email=self.normalize_email(email), **extra_fields)


Next we're going to add validation to ensure that an email field has actually been provided when the create_user function is called. We want to make sure that if we call the create_user funtion and we don;t pass an email address we raise a Value Error that says the email address was not provided

1. inside ModelTests class in test_models.py add new function called test_new_user_invalid_email.

2. Type:
    with self.assertRaise(ValueError):
        get_user_model().objects.create_user(None, 'testpass123')

    Anything that we run in here should raise the value error. And if it doesn't raise a ValueError then this test will fail.

test create superuser
1. Create test_create_superuser

Now that we have our create_user function finished thare's just one more function that we need to add to our user model manager and that is the create_superuser function. create_superuser is a function used bt the Django CLI when we're creating new users using the command line. So we want to make sure it's included in our custom User model so that we can take advantage of the Django managment command for creatin a superuser. We are goung to test that a sueruser is create when we call create_superuser thatt is assigned the is_staff an the is_superuser settings.
is_staff allows us to login to django admin site.
is_superuser allows us to have access to everythin in django admin

he reason why we didn't add is_superuser field in our User model but we add it here is is_superuser is included as part of the PermissionsMixin.

    test_create_super_user(self):
    """Test creating super user."""
    super_user = get_user_model().objects.create_superuser(
        email='testsuperuser@example.com',
        password='testpass123'
    )

    self.assertTrue(uuser.is_staff)
    self.assertTrue(user.is_superuser)

add this to UserManager

    def create_superuser(self, email, password):
      """Create and save new superuser."""
      user = self.create_user(email, password)
      user.is_staff = True
      user.is_superuser = True
      user.save(using=self._db)

      return user