# GoogleCalendarProject

## Overview

This repository contains a web app with the capabilities of using ai to create and post events on a personal google calendar

## Setup

Very first thing to do is go to google cloud under the group email and navigate to credentials.
Save the api key from Calendar Key 1 in a secure location (.env, .secure, etc.), I don't believe we will need this but better safe than sorry.

Next will be to generate a OAuth client, under the credentials tab again, click create credentials and select "OAuth Client ID." Set the application type to "Desktop app" and name it something unique, mine is "Desktop Client Elliott." The last step is to hit create and very importantly download the JSON file. We must rename the JSON file to "credentials.json" and add it to the route of your directory, this will be ignored by git.

We will then need to run several commands to get setup

1. `python -m pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client`

    This should install a .venv\ file

2. `.venv\Scripts\activate`

    This will direct the terminal into the virtual environment

3. `py generate_token.py`

    This will direct you into a browser on port 8080, log in using the group email to gain your token file


