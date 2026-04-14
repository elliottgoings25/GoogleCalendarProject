# GoogleCalendarProject

## Overview

This repository contains a web app with the capabilities of using ai to create and post events on a personal google calendar

## Setup

Will need to run several commands to get setup

1. `python -m pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client`

    This should install a .venv\ file

2. `.venv\Scripts\activate`

    This will direct the terminal into the virtual environment

3. `py generate_token.py`

    This will direct you into a browser on port 8080, log in using the group email to gain your token file

4. `deactivate`

    This will leave the virtual environment


