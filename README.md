# PyGrounds-API

A Python web-scraping API I wrote for Newgrounds. Currently, it only supports the audio portal, but I will be adding new features.

# Usage

## Author

Initialize an author object using the `Author` class.

``` Python
from PyGrounds import Author

# Case insensitive
geoxor = Author('geoxor')
```

### Attributes

| Attribute | Type | Information |
| - | - | :- |
| `exists` | Boolean | Whether or not the author was able to be found |
If `exists` is `True`:
| `name` | String | Author's username with accurate capitalization |
| `songs` | List | Ordered list of the ID's of all songs the author has published |

## Song

Initialize a song object using the `Song` class.

``` Python
from PyGrounds import Song

# Integer required
galaxy = Song(1006627)
```

### Attributes

| Attribute| Type | Information |
| - | - | :- |
| `exists` | Boolean | Whether or not the song was able to be found |
If `exists` is `True`:
| `ID` | Integer | ID of the song |
| `name` | String | Name of the song |
| `author` | String | Author of the song |
Newgrounds Statistics:
| `listens` | Integer | How many people have played the song |
| `faves` | Integer | How many people have favorited the song |
| `downloads` | Integer | How many people have downloaded the song |
| `votes` | Integer | How many people have rated the song |
| `score` | Float | Rating of the song, out of 5 (stars) |
| `genre` | String | What genre the author chose for the song |
Song statistics:
| `month` | Integer | What month the song was uploaded on |
| `day` | Integer | What day of the month the song was uploaded on |
| `year` | Integer | What year the song was uploaded on |
| `hour` | Integer | What military hour the song was uploaded on |
| `minute` | Integer | What minute, stripped of leading 0s, the song was uploaded on |
| `timeZone` | String | What timezone the song was uploaded in |
| `audioType` | String | What kind of audio it is, e.g. "Song", "Voice" |
| `size` | String | How many KB/MB the song is |
| `minutes` | Integer | How many minutes long the song is |
| `seconds` | Integer | How many seconds long the song is |
