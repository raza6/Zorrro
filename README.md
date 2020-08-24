# Zorrro ![Version](https://img.shields.io/github/v/release/raza6/Zorrro?include_prereleases)
Zorrro is a handy youtube-dl script with mp3 tagging.

Downloading music from youtube by hand is tedious and there is no service online to do such a task, so I developed my own script.

## Prerequisites
It uses youtube-dl, BeautifulSoup4, eyeD3, PySimpleGUI and requests python libraries (You will have to install them with pip).
`pip install youtube-dl beautifulsoup4 eyeD3 PySimpleGUI requests`

You also need a valid install of tkinter and ffmpeg.

## Usage
Launch it from command line with python 3: `python ./Zorrro-YtMP3.py`
* Use --ignore if you want to skip the youtube-dl version check.
* Use --loop if you want to be prompt for a new download when the previous one ended.

/!\ Disclaimer: the GUI is in french, have some baguette fun =P

All fields, except the first one, can remain empty.
Leaving the 'Album' field blank will set this tag to 'Autres'.
If you want to add a cover to your .mp3, put a link to an image in the cover field.

If you're downloading a playlist, the 'Titre' field is interpreted as a regex on the youtube title so that the first group of the regex becomes the title of your .mp3.
