# CHATIMUSMAXIMUS
[![Build Status](https://travis-ci.org/benhoff/CHATIMUSMAXIMUS.svg?branch=master)](https://travis-ci.org/benhoff/CHATIMUSMAXIMUS) [![Code Climate](https://codeclimate.com/github/benhoff/CHATIMUSMAXIMUS/badges/gpa.svg)](https://codeclimate.com/github/benhoff/CHATIMUSMAXIMUS)

## NOTE: All of the communication/adapter code has been moved to [vexbot](https://github.com/benhoff/vexbot)

A Python3.5, PyQt chat GUI featuring support for the following websites
> Youtube          (Selenium based scraper or Youtube API)
> Twitch           (IRC client)  
> WatchPeopleCode  (websocket client)  
> Livecoding       (xmpp client)


### Installation instructions
1. `pip install chatimusmaximus`
4. create a settings.yml file using `default_settings.yml` as guidance
5. `chatimusmaximus --settings_path /path/to/your/settings.yml`

### Alternatively clone/download and unzip, change into directory
1. `pip install -r requirements.txt`
2. `python setup.py develop`
3. `python chatimusmaximus`

If you run into issues, send me an email [beohoff@gmail] or start an issue!

### Running instructions
1. change into the `chatimusmaximus` source directory and from the command line run `python chatimusmaximus`
2. Or run the code from vexbot `https://github.com/benhoff/vexbot.git`. I haven't had time to write up running instructions for vexbot :shame: but feel free to email me about it.

pull requests welcome!

Chatimusmaximus uses [Click](http://www.freesound.org/people/lebcraftlp/sounds/192278/) from [lebcraftlp](http://www.freesound.org/people/lebcraftlp/).
