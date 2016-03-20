# CHATIMUSMAXIMUS
[![Build Status](https://travis-ci.org/benhoff/CHATIMUSMAXIMUS.svg?branch=master)](https://travis-ci.org/benhoff/CHATIMUSMAXIMUS) [![Code Climate](https://codeclimate.com/github/benhoff/CHATIMUSMAXIMUS/badges/gpa.svg)](https://codeclimate.com/github/benhoff/CHATIMUSMAXIMUS)

A Python3.5, PyQt, read-only, client, chat GUI featuring support for the following websites
> Youtube          (Selenium based scraper)  
> Twitch           (IRC client)  
> WatchPeopleCode  (websocket client)  
> Livecoding       (xmpp client)

### Installation instructions
1. Install PyQt5 onto your system
2. Install PhantomJS onto your system
3. Clone the library or download and unpack the tar.gz file and change to that directory
4. install the required libraries (`pip install -r requirements.txt`)
5. setup to run in develop mode (`python setup.py develop`)
6. change the default settings to suit your needs, optionally copying into a new file named `settings.yml`

### Running instructions
1. change into the `chatimusmaximus` source directory and from the command line run `python chatimusmaximus`

pull requests welcome!
