# Backend
Backend for our ECSE 428 application

# Development Setup
We're using python 3+ with django v2. 
Ensure that the python and pip versions you use are configured 
for python 3+.

### Configure VirtualEnv
VirtualEnv ensures that you will have an isolated environment for this project

To create a new virtualenv
```
pip install virtualenv
virtualenv env
```

To activate the virtual env from a bash command line use
```
source env/bin/activate
```

### Install the Project Dependencies

Ensure you're in the virtual environment for the project, then run
```
pip install -r requirements.txt
```

### Configuring MySQL and Redis with Docker Compose

You'll need to run MySQL and Redis on localhost in order for the app to work. With docker compose this is as simple as running
```
docker-compose up
```

If you're running using a docker-machine VM then set the environment variables so that when you run the app locally
it'll know where to reach the machine.
```
MYSQL_HOST=*Insert Docker VM IP here*
REDIS_HOST=*Insert Docker VM IP here*
```

### Installing New Packages

If you require a new package during development, ensure that you add a line for it in requirements.txt. 
If you're working in a virtualenv, then you can also run the to update the requirements.txt file.

##### Don't do this if you're not using a virtualenv or you'll get a slap
```
pip freeze > requirements.txt
```

# Testing

Go into the timemachine folder

```
cd timemachine/
python manage.py test
```

# Style Checking & Linting

```
./test.sh
```

