# Music Application

- The general approach taken was to have an Artist user along with a Consumer user, who can add songs and albums to make it more intuitive.
- The recommendation approach was content based recommendation since collaborative filtering needs lots of data. Similarity scores were calculated between two songs based on album/artist/genre and ranked them in decreasing order of their scores. 
- The goal was to recommend users songs similar to their playlists but not in their playlist to avoid having the same songs again and again. However, if the system runs out of new songs to recommend the current playlists songs are taken into consideration to match the required playlist length.
- Another recommendation strategy for categories alone (e.g. only genre based songs, artist based songs) was to find out the likeliness of the user to listen to the same genre which was calculated by numOfSongsWithCategory/totalNumOfSongs. This was used when songs were to be recommended on genre alone or artist alone or album alone.
- The postman collection for testing has been added for testing.

### Installation


Install the dependencies and start the server.

```sh
$ git clone https://github.com/Mihir-Karbelkar/Music.git
$ cd Music
$ pip install -r requirements.txt
$ python manage.py runserver
```
