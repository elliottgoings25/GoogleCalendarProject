# GoogleCalendarProject

## Overview

This repository contains a desktop app with the capabilities of using ai to create and post events on a personal google calendar

## Setup

Very first thing to do is go to google cloud under the group email and navigate to credentials.
Save the api key from Calendar Key 1 in a secure location (.env, .secure, etc.), I don't believe we will need this but better safe than sorry.

Next will be to generate a OAuth client, under the credentials tab again, click create credentials and select "OAuth Client ID." Set the application type to "Desktop app" and name it something unique, mine is "Desktop Client Elliott." The last step is to hit create and very importantly download the JSON file. We must rename the JSON file to "credentials.json" and add it to the route of your directory, this will be ignored by git.

We will then need to run several commands to get setup

1. `py -m venv .venv`

    This should install a .venv\ file

2. `.venv\Scripts\activate`

    This will direct the terminal into the virtual environment

3. `python -m pip install PyQt5 pyinstaller google-auth google-auth-oauthlib google-api-python-client`

    This will download the files needed for setup of tokens and ui interface

From there, as long as you have the credentials file and previous commands ran, running the program should automatically call the token generator to establish a connection to google


also here is a .exe build command if you want it
    `pyinstaller --onefile --windowed --icon=CPSC311.ico --add-data ".env;." main.py`