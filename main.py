# Coded by Ryan Dodd. This application is intended to clean empty folders from a directory.
import os
from datetime import datetime
import time
import re
import PySimpleGUI as sg # What displays to make the program usable.

# Console runner code: python -m main

Path = ""
CheckSubDir = True
DeleteOffCreation = True
Date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

FoldersRemoved = 0
FolderRemovalErrors = []

# How the program looks.
Layout = [
    [sg.Text("This application clears empty folders from a directory.")],
    [sg.Text("Choose a directory to clean: "), sg.Input(key="DIRECTORY", enable_events=True), sg.FolderBrowse(target="DIRECTORY")],
    [sg.Text("Do you want to check subdirectories for empty folders as well?"), sg.Checkbox("", key="SUBDIR", default=True, enable_events=True)],
    [sg.Text("Delete files based off creation date? (will use modified date otherwise)"), sg.Checkbox("", key="CREATION", default=True, enable_events=True)],
    [sg.Text("Date: "), sg.Input(key="DATE", enable_events=True, default_text=Date), sg.CalendarButton("Choose Date", target="DATE", format="%m/%d/%Y %H:%M:%S")],
    [sg.Button("Clean Files", key="CLEAN", disabled=True), sg.Text("This may take awhile depending on your settings. Please be patient.", key="CLEANING_TEXT")],
]

Window = sg.Window(title="File Cleaner", layout=Layout, resizable=True, finalize=True)

def validateDate(DateText):
    try:
        datetime.strptime(DateText, "%m/%d/%Y %H:%M:%S")
        return True
    except ValueError:
        return False

def getFileDate(FilePath):
    if DeleteOffCreation:
        return time.ctime(os.path.getctime(FilePath))
    else:
        return time.ctime(os.path.getmtime(FilePath))

def tryRemoving(RemovalPath):
    global FoldersRemoved
    global FolderRemovalErrors
    try:
        os.rmdir(RemovalPath)
        FoldersRemoved = FoldersRemoved + 1
    except OSError as error:
        FolderRemovalErrors.append(error)

#Recursively will check files and remove them (provided that the option is checked).
def recursivelyCheckAndRemove(FilePath, EnteredTime):
    FileTimeAsDateTime = datetime.strptime(getFileDate(FilePath), "%a %b %d %H:%M:%S %Y")
    if FileTimeAsDateTime < EnteredTime and os.listdir(FilePath) == []:
        tryRemoving(FilePath)
    elif FileTimeAsDateTime < EnteredTime and CheckSubDir:
        # Checks the subdirectory
        for File in os.listdir(FilePath):
            if os.path.isdir(FilePath + "/"+ File) and not os.path.isfile(File):
                recursivelyCheckAndRemove(FilePath + "/"+ File, EnteredTime)

        # Checks the current directory again. If empty, removes it. Otherwise, it will continue to exist.
        if os.listdir(FilePath) == []:
            tryRemoving(FilePath)

while True:
    Event, Values = Window.read()
    if Event == sg.WIN_CLOSED or Event in (None, 'Exit'):
        break
    elif Event == "DIRECTORY":
        Window.find_element("CLEAN").update(disabled=True)
        Path = Values["DIRECTORY"]
        if Path != "" and os.path.exists(Path):
            Window.find_element("CLEAN").update(disabled=False)
    elif Event == "SUBDIR":
        CheckSubDir = Values["SUBDIR"]
    elif Event == "CREATION":
        DeleteOffCreation = Values["CREATION"]
    elif Event == "DATE":
        Window.find_element("CLEAN").update(disabled=True)
        Date = Values["DATE"]
        if Date != "" and validateDate(Date):
            Window.find_element("CLEAN").update(disabled=False)
    elif Event == "CLEAN":
        FolderRemovalErrors = []
        FoldersRemoved = 0
        for File in os.listdir(Path):
            if os.path.isdir(Path + "/"+ File) and not os.path.isfile(File):
                SplitTimeEnter = re.split(' |:|/', Date)
                EnteredTime = datetime(month=int(SplitTimeEnter[0]), day=int(SplitTimeEnter[1]), year=int(SplitTimeEnter[2]), hour=int(SplitTimeEnter[3]), minute=int(SplitTimeEnter[4]), second=int(SplitTimeEnter[5]))
                recursivelyCheckAndRemove(Path + "/"+ File, EnteredTime)
        Window.find_element("CLEANING_TEXT").update("Completed cleaning files. " + str(FoldersRemoved) + " folders removed. Errors: " + str(FolderRemovalErrors))

Window.close()