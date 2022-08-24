from urllib.request import urlopen, Request
from urllib.error import HTTPError
from threading import Thread
from html import unescape
from re import finditer

# Make GET requests easier to parse
def getPageData(url):
    return urlopen(url).read().decode()

# Function for getting content between two strings
def getBetweenStrings(string, before, after, removeCommas=False, toInt=False):
    try:
        item = string.index(before) + len(before)
        item = string[item:]
        item = item[:item.index(after)]

        if removeCommas:
            item = item.replace(',', '')

        if toInt:
            return int(item)

        return unescape(item)
    
    except:
        # String was not found
        return 'NA'

# List of months' abbreviations and their numbers
abbreviations = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
months = {month: num + 1 for num, month in enumerate(abbreviations)}

class Author:
    def __init__(self, name):
        # Check if the author exists
        try:
            self.pageData = getPageData(f'https://{name}.newgrounds.com/audio')
            self.name = getBetweenStrings(self.pageData, '<title>', '<')[:-8]
            self.exists = True

            # List the IDs of the author's published songs
            self.getSongs()
            
        except HTTPError as error:
            error = str(error)

            if '404' in error:
                self.exists = False
                self.name = None
                self.songs = []

    def getSongs(self):
        IDIndexes = [i.start() + 40 for i in finditer('https://www.newgrounds.com/audio/listen/', self.pageData)]
        truncatedPageData = [self.pageData[i:] for i in IDIndexes]
        IDs = [int(i[:i.index('"')]) for i in truncatedPageData]

        # Remove duplicates (caused by the Highlights section) and sort
        newIDs = []
        for ID in IDs:
            if ID not in newIDs:
                newIDs.append(ID)
        newIDs.sort()

        self.songs = newIDs

class Song:
    def __init__(self, ID):
        self.ID = ID

        # Check if the song exists
        try:
            self.pageData = getPageData(f'https://www.newgrounds.com/audio/listen/{self.ID}')
            self.exists = True

            # Self explanatory
            self.getNameAndAuthor()
            self.getNGStats()
            self.getSongStats()
            
        except HTTPError as error:
            error = str(error)

            if '404' in error:
                self.exists = False

    def getNameAndAuthor(self):
        # Get the song name from the <title> tag
        self.name = getBetweenStrings(self.pageData, '<title>', '<')

        # Get the song author from the JS embedController
        author = getBetweenStrings(self.pageData, '"artist":"', '"')
        self.author = author

    def getNGStats(self):
        # Simply find the stats in the <dd> tags
        self.listens = getBetweenStrings(self.pageData, '<dt>Listens</dt>\n\t\t\t<dd>', '<', True, True)
        self.faves = getBetweenStrings(self.pageData, 'id="faves_load">', '<', True, True)
        self.downloads = getBetweenStrings(self.pageData, '<dt>Downloads</dt>\n\t\t\t\t<dd>', '<', True, True)
        self.votes = getBetweenStrings(self.pageData, '<dt>Votes</dt>\n\t\t\t\t<dd>', '<', True, True)
        self.score = float(getBetweenStrings(self.pageData, '<span id="score_number">', '<', True))
        genre = self.pageData[self.pageData.index('data-genre-for="'):]
        self.genre = getBetweenStrings(genre, '>', '<')

    def getSongStats(self):
        # Parse the uploaded date into day, month, year, time and timezone
        uploaded = getBetweenStrings(self.pageData, '<dt>Uploaded</dt>\n\t\t<dd>', 'T</dd>', True)
        date = uploaded[:uploaded.index('<')].split(' ')
        time = uploaded[int(uploaded.index('<') + 12):].split(' ')

        self.month = months[date[0]]
        self.day = int(date[1])
        self.year = int(date[2])

        oClock = time[0].split(':')
        # Convert to military time
        if time[1] == 'PM':
            oClock[0] = int(oClock[0]) + 12
        self.hour = int(oClock[0])
        # Strip minutes section of trailing 0
        if oClock[1][0] == '0':
            oClock[1] = oClock[1][1:]
        self.minute = int(oClock[1])
        self.timeZone = time[2] + 'T'

        # Cut off everything before where the file info starts
        fileInfo = self.pageData[self.pageData.index('<dt>File Info</dt>\n\t\t\t\t\t\t\t<dd>\n\t\t\t\t\t\t\t\t\t\t\t') + 42:]
        self.audioType = fileInfo[:fileInfo.index('<')].strip()

        fileInfo = fileInfo[fileInfo.index('</dd>\n\t\t\t\t\t\t\t<dd>\n\t\t\t\t\t\t\t\t\t\t\t') + 29:]
        # Remove the <span> tags to get just the gooey filesize in the center
        self.size = fileInfo[:fileInfo.index('</span>')].replace('<span>', '')

        fileInfo = fileInfo[fileInfo.index('</dd>\n\t\t\t\t\t\t\t<dd>\n\t\t\t\t\t\t\t\t\t\t\t') + 29:]
        duration = fileInfo[:fileInfo.index('c')].split(' ')
        del duration[1], duration[2]
        duration = [int(i) for i in duration]
        # Duration shown in the file info section is always 1 second shorter
        duration[1] += 1
        if duration[1] == 60:
            duration[0] += 1
            duration[1] = 0
            
        self.minutes, self.seconds = duration

    def download(self, location):
        # Retrieve song data
        songData = urlopen(f'https://www.newgrounds.com/audio/download/{self.ID}').read()

        # Write to file
        fullPath = f'{location}/{self.ID}.mp3'

        with open(fullPath, 'wb') as file:
            file.write(songData)
