# doc-app-api
Documents app api source code.

 ### Starting GitHub Project
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


 ### Authenticate with Dockerhub
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

### Configure Docker
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

### Creating requirements.txt file
This is a list with all python requirements for this project.
Django >=4.1,<4.2 - This make supre tah the patch versioni s alvays up to date

### Adding Dockerfile
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

    >  WHY WE ARE TRYING MAKE LESS LAYERS IF DOCKERFILE ??
        How venv works
        what is pycache


