🎵 Music CMD

Music CMD is a simple command-line music player that lets you organize your music by artists and albums, then play them directly from the terminal.

📁 Folder Structure

To add your own music, just follow this structure:

📂 MusicCMD/
│
├── main.py
│
├── 📂 ArtistName/
│   ├── song1.mp3
│   ├── song2.mp3
│   └── 📂 AlbumName/
│       ├── track1.mp3
│       └── track2.mp3


Each artist should have their own folder in the same directory as main.py.

Inside each artist folder, you can place individual songs or full album folders.

🎮 Commands

You can control playback with simple commands right from the console.
Type !help at any time to see the list of available commands.

Command	Description
play X	Play song number X
pause	Pause or resume playback
stop	Stop playback
next	Play the next song
prev	Play the previous song
set volume X	Set volume to X% (0–100)
list	Show the current song list
repeat song	Repeat the current song
repeat album	Repeat the entire album
repeat off	Turn off repeat mode
change_artist	Switch to a different artist
change_album	Switch to a different album
exit	Exit the program
!help	Show all available commands
