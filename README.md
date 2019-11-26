# sound-annotator
PyQt5 GUI for annotating sound events manually from a spectrogram.

This application is not perfect, but is use-able. I have only tested it on macOS (Mojave and Catalina). The application is meant to look at wav files and works best for those created by AudioMoth.  

## Set up
Clone the repo. For help see https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository. 

Create a virtual environment and activate it. For help see https://docs.python.org/3/tutorial/venv.html.

Install pip if needed. https://pip.pypa.io/en/stable/installing/

Download dependencies by running:
`pip install -r requirements.txt`

To run program:
`python3 main.py`

![Alt text](/screenshots/start.png?raw=true "Starting Screen")

## Start a new session
File -> New Session

This opens a dialog box where you can type or choose the data path (where the wav files are) and then the save path (a new filename which will be a csv file where annotations will be saved). 

Mininum Duration will force selections to be at least that many seconds long.

![Alt text](/screenshots/new_session.png?raw=true)

## Load a previous session
File -> Load Session

This opens a file browser where you need to select a configuration file (.yaml). It will open the session to the file you left off on and it will continue saving to the same save file. 

## Create an annotation
Drag the mouse over a part of the spectrogram. Press the play button or Action -> Play to listen to the selection. Press the save button or Action -> Save to save an annotation.

![Alt text](/screenshots/create_anno.png?raw=true)

## Edit an annotation
Find the information you would like to edit in the table. Click on an entry to edit it. The original csv file is changed to match when you click elsewhere. Currently there is no way to delete a row but you can erase the entry. 

![Alt text](/screenshots/edit_tag.png?raw=true)

## Move to a different file
Use the previous and next button or Action -> Previous and Action -> Next. 

## Save a session
Saving a session is for convenience. It does not affect whether the csv file is saved or not because the annotations are always saved the moment they are created. 

Python -> Quit Python

This brings up a dialog box where you are given the option to save the current session. If you choose yes you provide a filename and choose where to save it. 

![Alt text](/screenshots/save_session.png?raw=true)

Warning: If you press the "x" button the application will close without saving your session (however your annotations are saved the moment you create them).

## Browse audio files visually
Create a session normally and use a dummy save file.  

## Forgot to save session but want to continue annotating 
Simply start a new session again and instead of creating a new save file select the one you were using before (for some reason the dialog box will disappear behind the application, just move the application out of the way and press ok on the box). By default, the spectrogram shown will be the first. You can use Actions -> Goto to skip ahead. 




