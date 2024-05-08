# Berlin Ausländerbehörde Termin Bot

A fork of https://github.com/yinwu33/berlin-auslanderbehorde-termin-bot which itself is a fork of https://github.com/capital-G/berlin-auslanderbehorde-termin-bot.

* Operates on the English version of the LEA's TerminBuchen-Page.
* Should run on macOS, Windows and Linux.
* Preconfigured for: first application / Israel citizen / one person w/o family / economic activity / freelance. Examples for other countries and purposes in comments.

## Disclaimer:

I am no software developer but merely something like a script kiddie.

## Setup

* Install Chrome Browser (or update it if already installed)
* Install python and git
* `git clone https://github.com/assel/berlin-auslanderbehorde-termin-bot.git`
* Setup a virtualenv via `virtualenv venv` and activate it (see below)
* Install dependencies via `pip3 install -r requirements.$yourOS.txt`
* Put a `chromedriver` binary from <https://chromedriver.chromium.org/downloads> into the directory. Those work for me:
    * linux64:	https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.155/linux64/chromedriver-linux64.zip
    * mac-x64:	https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.155/mac-x64/chromedriver-mac-x64.zip
    * win64:	https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.155/win64/chromedriver-win64.zip
* Configure `berlin_bot.py` according to your needs (see below)
* Start the bot via `python3 berlin_bot.py`

### venv for dummies
Excample (how I run it on my macBook):
 `MacBook-Pro-3:~ assel$ pwd`
`/Users/assel`
`MacBook-Pro-3:~ assel$ cd berlin-auslanderbehorde-termin-bot/`
`MacBook-Pro-3:berlin-auslanderbehorde-termin-bot assel$ python3 -m venv venv`
(Chromedriver belongs to venv/bin)
`MacBook-Pro-3:berlin-auslanderbehorde-termin-bot assel$ . venv/bin/activate`
(Windows: venv\Scripts\activate)
`(venv) MacBook-Pro-3:berlin-auslanderbehorde-termin-bot assel$ python3 berlin_bot.py`

## Configuration and Support

I do not give any kind of support and/or advice on how to configure this bot.
You can read the [selenium docs](https://selenium-python.readthedocs.io/locating-elements.html#) and adjust `berlin_bot.py` in order to configure it according to your needs.
Use Chrome:s developer extensions to find out the the names or paths of the elements the script is supposed to click on.

## License

AGPL-3.0

# Original README.md below:

A [Selenium](https://www.selenium.dev/) bot for obtaining an appointment at the [Landesamt für Einwanderung](https://otv.verwalt-berlin.de/ams/TerminBuchen) aka Ausänderbehörde in Berlin.

I did not want to open source this as this makes it harder for the people without IT knowledge to obtain an appointment, but as there are already people who make a benefit of this (50 euro per appointment!) I thought it would be a good thing to make the tools available to everyone. This project is therefore a counter measurement against those people as well as the inability of the Ausländerbehörde to provide sufficient appointments.

Take a look at the video [Hinter verschlossenen Türen – Mysterium Ausländerbehörde - ZDF Magazin Royale
](https://www.youtube.com/watch?v=s7HrAGlni50) to find out more about the bad shape of this agency.

## Setup

* `git clone https://github.com/capital-G/berlin-auslanderbehorde-termin-bot.git`
* Setup a virtualenv via `virtualenv venv` and activate it
* Install dependencies via `pip3 install -r requirements.txt`
* Put a `chromedriver` binary from <https://chromedriver.chromium.org/downloads> into the directory
* Configure `berlin_bot.py` according to your needs (see below)
* Start the bot via `python3 berlin_bot.py`

## Configuration and Support

I do not give any kind of support and/or advice on how to configure this bot as I wrote this for a friend of mine and thankfully she was able to get an appointment with this bot.
You can read the [selenium docs](https://selenium-python.readthedocs.io/locating-elements.html#) and adjust `berlin_bot.py` in order to configure it according to your needs.

## License

AGPL-3.0
