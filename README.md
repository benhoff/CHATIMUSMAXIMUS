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

### Socket Address?
Chatimusmaximus uses messaging and subprocesses for different services. This has some advantages/disadvantages of this approach, but the reason it's staying is it allows the developer some decreased congnitive load while developing this project.

The socket address expected is in the format of `tcp://[ADDRESS]:[PORT_NUMBER]`. 
For example `tcp://127.0.0.1:5617` is a valid socket address. 127.0.0.1 is the ADDRESS and 5617 is the PORT_NUMBER. 

#### TCP address
127.0.0.1 was chosen specifially as an example because for IPV4 it is the "localhost". Localhost is the computer the program is being run on. So if you want the program to connect to a socket on your local computer (you probably do), use 127.0.0.1.

#### Ports
Port numbers range from 0-65536, and can be mostly aribratry chosen. For linux ports 0-1024 are reserved, so best to stay away from those. Port 5555 is usually used as an example port for coding examples, so probably best to stay away from that as well.

If you run into issues, send me an email [beohoff@gmail] or start an issue!

### Running instructions
1. change into the `chatimusmaximus` source directory and from the command line run `python chatimusmaximus`

pull requests welcome!
