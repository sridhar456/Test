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
