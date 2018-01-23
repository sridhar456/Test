# Python API Samples
Python examples of how to use the Looker API

## What you can find here
- A simple Looker API 3.0 SDK
- A sample config.yml file for collecting API Tokens/Secrets
- Sample files of various tasks using the API

## Relevant Articles
**Moving Looks**: https://discourse.looker.com/t/moving-a-look-between-looker-servers-using-the-looker-api-and-the-python-requests-library/

## Getting Started
- Copy at minimum the configration_sample.yml and lookerapi.py files.
- Change the config_sample.yml to config.yml and update with your credentials
- Run any file in the shell with `python <<filename>>`

## Scripts

|File|Description|How to|
|----|----|----|
|delete_look.py|Illustrates how to delete a look or a list of looks delimited by newlines|Make sure you have the host in your config.yml file and adjust the source look variables at the top of the script.
|delete_dashboard.py|Illustrated how to delete a dashboard or a list of dashboards delimited by newlines|Make sure you have the host in your config.yml file and adjust the source look variables at the top of the script.
|get_look.py|Illustrates how to get the data from a look|Make sure you have the host in your config.yml file and adjust the source look variables at the top of the script.|
|move_look.py|Illustrates how to move a look between servers, or between the same server|Make sure you have both hosts in your config.yml file and adjust the source look, destination space variables at the top of the script.|
|get_data_dictionary.py|Put together a list of each field, and various attributes in your data model, this outputs a CSV|Make sure your host is configured in the config.yml file|
|update_user.py|Update user parameters with a CSV| In the script, reference a CSV which maps individual user IDs to whichever user parameters you would like to update. Use the `/users/{user_id}/credentials_email` endpoint to update email/password login information.|
|update_static_filter.py|Update a static filter value on a look| Illustrates how to update a static value associated with a filter field|
|delete_expired_schedules.py|Delete schedules that have an expiry date in the title|Gets a list of all schedules and then checks the title for an expiry date specified in the title.  If the current date is past that date, delete the schedule|

