# SSSBReminder

#### Introduction

This project is composed of three parts:

- A web crawler that regularly collects housing information from sssb.se
- A web page where users can create their own apartment filters
- A filter executor that sends an email to the user whenever the user's conditions are met

#### Requirements

- selenium
- django
- mongodb (pymongo)

#### Run

To run the project, run following commands simultaneously (recommended on a server, probably in a tmux session)

```bash
python check_sssb.py --endless --headless --get_url  
python check_sssb.py --endless --headless --check_url
python check_sssb.py --endless --headless --check_filter
```

By default, the script will collect housing information and check filters every 30 minutes.

Also run following command to run the web page server

```bash
cd SSSB
python manage.py runserver 0.0.0.0:8000
```

Open [localhost](http://localhost:8000) in your browser.