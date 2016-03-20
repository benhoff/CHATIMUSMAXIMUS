# CHATIMUSMAXIMUS
[![Build Status](https://travis-ci.org/benhoff/CHATIMUSMAXIMUS.svg?branch=master)](https://travis-ci.org/benhoff/CHATIMUSMAXIMUS) [![Code Climate](https://codeclimate.com/github/benhoff/CHATIMUSMAXIMUS/badges/gpa.svg)](https://codeclimate.com/github/benhoff/CHATIMUSMAXIMUS)

A Python3.5, PyQt chat GUI featuring support for the following websites
> Youtube          (Selenium based scraper)  
> Twitch           (IRC client)  
> WatchPeopleCode  (websocket client)  
> Livecoding       (xmpp client)

### Installation instructions
1. Install PyQt5 onto your system
2. Install PhantomJS onto your system
3. `pip install chatimusmaximus[gui,javascript_webscrapper,irc,socket_io,xmpp,youtube]`
4. create a settings.yml file using `default_settings.yml` as guidance
5. `chatimusmaximus --settings_path /path/to/your/settings.yml`

### Alternatively clone/download and unzip, change into directory
1. `pip install -r requirements.txt`
2. `python setup.py develop`
3. `python chatimusmaximus`

If you run into issues, send me an email [beohoff@gmail] or start an issue!

### Running instructions
1. change into the `chatimusmaximus` source directory and from the command line run `python chatimusmaximus`

pull requests welcome!
