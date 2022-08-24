__doc__ = '''Arguments:
    -help       Shows this screen

    -author "<name>"        Accesses an author with the given name. Case insensitive, must be double quotes
        -list               List the IDs of every song the author has published
        OR
        -download "<path>"      Download all of the author's songs into the given path. Must have double quotes
                                - File format: <song ID>.mp3
                                - Can be relative or absolute, will be detected

    -song "<song ID>"           Accesses a song with the given ID. Must be in double quotes
        -info                   Display all available info on the song
        OR
        -download "<file path>"     Download the song to the file path. Must be in double quotes
                                    - File name and MP3 format must be specified
                                    - Can be relative or absolute, will be detected

    -download "<song ID 1>" "<song ID 2>" "<path>"      Download all songs to the designated path
                                                        - Each song ID  and the path must be in double quotes
                                                        - Path can be relative or absolute, will be detected'''
from PyGrounds import Author, Song

from urllib.request import urlretrieve
from urllib.error import HTTPError
from colorama import init, Fore
from time import sleep
from os import getcwd
from sys import argv

# Wrapper functions for downloading
def printProgressBar(a, b, c):
    progress = round((a * b) / c * 40)

    bar = f'\r[{Fore.GREEN}{progress*"#"}{Fore.RESET}{(40-progress)*" "}]'
    bar += f' | {a}/{int(c/b)} chunks transferred'

    print(bar, end='')
    
def downloadSong(ID, filePath):
    try:
        # Good ending
        urlretrieve(f'https://www.newgrounds.com/audio/download/{ID}', filePath, printProgressBar)
        return 400
    
    except HTTPError as error:
        # Bad ending (return error code)
        return int(str(error).split(' ')[2][:-1])

# Make colored text work
init(convert=True)

# Get a list of arguments
arguments = argv[1:]

if arguments[0] == '-help':
    print(__doc__)

elif arguments[0] == '-author':
    name = arguments[1]

    command = arguments[2]
    if command == '-list':
        print(f'Listing {name}\'s songs...', end='')
        author = Author(name)
        
        print(f'\n - '.join(str(ID) for ID in author.songs))

    elif command == '-download':
        path = arguments[3].strip('/').strip('\\')
        
        if ':' not in path:
            path = f'{getcwd()}\{path}'

        print(f'Getting {name}\'s songs...', end='')
        author = Author(name)

        urls = [f'https://www.newgrounds.com/audio/listen/{ID}' for ID in author.songs]
        filePaths = [f'{path}\\{ID}.mp3' for ID in author.songs]

        for url, filePath, ID in zip(urls, filePaths, author.songs):
            print(f'\n\nDownloading song {ID} to {filePath}...')

            statusCode = None
            while statusCode != 400:
                statusCode = downloadSong(ID, filePath)

                if statusCode == 429:
                    print(f'{Fore.RED}[!] HTTP Error 429: Too many requests {Fore.RESET}| Waiting 20 seconds to resolve...')
                    sleep(20)

elif arguments[0] == '-song':
    songID = int(arguments[1])

    command = arguments[2]
    if command == '-info':
        print(f'\nListing information on song {songID}...\n')
        song = Song(songID)

        if song.exists:
            print(f'"{song.name}" by {song.author}\n')
            print(f'Listens: {song.listens}\t\tUploaded: {song.month}/{song.day}/{song.year}, {song.hour}:{song.minute} {song.timeZone}')
            print(f'Faves: {song.faves}')
            print(f'Downloads: {song.downloads}')
            print(f'Votes: {song.votes}')
            print(f'Score: {song.score}')

        else:
            print(f'{Fore.RED}[!] Error 404: Song not found')
