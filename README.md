# `pygrounds` - Python Newgrounds API

This is the first implementation of a Newgrounds API written in Python.

# `Audio`

## Initialization

```python
song = Audio(533927)
```

## Attributes

### `id` (`int`)

The song ID.

### `name` (`str`)

The song name.

### `artists` (`list`)

A list of the song's artists.

### `artist` (`str`)

The song's primary artist.

### `listens` (`int`)

Amount of listens on the song.

### `votes` (`int` | `None`)

Amount of votes on the song.

### `faves` (`int` | `None`)

Amount of faves on the song.

### `score` (`float` | `None`)

The song's score, as a proportion.

### `genre` (`str`)

The song's genre.

### `date_published` (`datetime`)

The date and time the song was published.

### `audio_type` (`str`)

Type of audio, e.g. `"loop"`, `"podcast"`

### `file_size` (`str`)

Human-readable file size of the song.

### `duration` (`int`)

Duration of the song in seconds.

### `tags` (`list`)

List of the song's tags.

### `author_comments_html` (`str` | `None`)

Author comments section as HTML code.

### `short_description` (`str` | `None`)

A short description of the song.

### `frontpaged` (`bool`)

Whether or not the song was ever frontpaged.

### `date_frontpaged` (`datetime` | `None`)

The date the song was frontpaged.

### `download_url` (`str`)

Download URL for the song.

### `track_image` (`str`)

URL for the track image of the song.

### `refresh` (method)

Refreshes all information on the song.
