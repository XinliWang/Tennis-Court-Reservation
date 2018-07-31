# Tennis-Reservation
## Description
This application is designed for tennis court reservation online.  The tennis court will be reserved every day at specific time automatically.

## Run the app locally
python version: `3.6`

1. `create account.txt`

  - username = \<username\>
  - password = \<password\>
  - url = \<url\>

2. `virtualenv tennis`

3. `source tennis/bin/activate`

4. `pip install -r requirements.txt`

5. `setup the timer in main.py for reservation and cancellation`

6. `python main.py`

## Run the app in Docker and deploy

1. `docker build -t tennis .`

2. `docker run -d tennis`
