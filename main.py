import os
import pygame
import sys

pygame.mixer.init()

current_dir = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))

current_song = None
current_index = None
paused = False
repeat_mode = "none"
current_dir_song = None
songs = []
artist_dir = None

commands_help = {
    "play X": "Play song number X",
    "pause": "Pause / resume",
    "stop": "Stop playback",
    "next": "Next song",
    "prev": "Previous song",
    "set volume X": "Set volume to X% (0–100)",
    "list": "Show song list",
    "repeat song": "Repeat current song",
    "repeat album": "Repeat album",
    "repeat off": "Turn off repeat",
    "change_artist": "Change artist",
    "change_album": "Change album",
    "exit": "Exit program",
    "!help": "Show commands"
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_cat():
    cat = [
        "        |\\      _,,,---,,_",
        "ZZZzz  /,`.-'`'    -.  ;-;;,_",
        "     |,4-  ) )-,_. ,\\ (  `'-'",
        "    '---''(_/--'  `-'\\_)",
        "", "", ""  # spaces for commands
    ]
    for line in cat:
        print(line)

def choose_dir(prompt, base_dir):
    items = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    if not items:
        print("No folders found.")
        return base_dir
    while True:
        clear_screen()
        print_cat()
        print(prompt)
        for i, name in enumerate(items, 1):
            print(f"{i}. {name}")
        try:
            choice = int(input("Enter number: ")) - 1
            if 0 <= choice < len(items):
                return os.path.join(base_dir, items[choice])
        except:
            pass
        print("Invalid choice. Try again.")
        input("Press Enter to continue...")

def list_songs():
    clear_screen()
    print_cat()
    if current_song:
        print(f"Now playing: {os.path.splitext(current_song)[0]}\n")
    print("Song list:")
    for i, song in enumerate(songs, 1):
        print(f"{i}. {os.path.splitext(song)[0]}")
    print()

def play_song(index):
    global current_song, current_index, paused
    if 1 <= index <= len(songs):
        pygame.mixer.music.load(os.path.join(current_dir_song, songs[index-1]))
        pygame.mixer.music.play()
        current_song = songs[index-1]
        current_index = index
        paused = False
        clear_screen()
        print_cat()
        print(f"Playing: {os.path.splitext(current_song)[0]}")
    else:
        print("Invalid song index.")

def handle_repeat():
    global current_index
    if repeat_mode == "song":
        play_song(current_index)
    elif repeat_mode == "album":
        next_index = current_index + 1
        if next_index > len(songs):
            next_index = 1
        play_song(next_index)

# Main loop
while True:
    artist_dir = choose_dir("Select artist:", current_dir)
    current_dir_song = choose_dir("Select album:", artist_dir)
    songs = [f for f in os.listdir(current_dir_song) if f.lower().endswith(('.mp3', '.ogg'))]
    if not songs:
        print("No songs found.")
        input("Press Enter to continue...")
        continue
    list_songs()

    current_song = None
    current_index = None
    paused = False
    repeat_mode = "none"

    while True:
        if current_song and not pygame.mixer.music.get_busy() and not paused:
            handle_repeat()
        try:
            cmd = input("Enter command (!help): ").strip().lower()
        except KeyboardInterrupt:
            pygame.mixer.music.stop()
            exit()

        if cmd == "!help":
            clear_screen()
            print_cat()
            print("Command list:")
            for k, v in commands_help.items():
                print(f"{k} - {v}")
            continue

        elif cmd.startswith("play"):
            try:
                idx = int(cmd.replace("play", "").strip())
                play_song(idx)
            except:
                print("Invalid command. Example: play2 or play 2")

        elif cmd == "pause" and current_song:
            if not paused:
                pygame.mixer.music.pause()
                paused = True
                print("Paused")
            else:
                pygame.mixer.music.unpause()
                paused = False
                print("Resumed")

        elif cmd == "stop" and current_song:
            pygame.mixer.music.stop()
            current_song = current_index = None
            paused = False
            print("Stopped")

        elif cmd == "next" and current_index:
            play_song(current_index + 1 if current_index + 1 <= len(songs) else 1)

        elif cmd == "prev" and current_index:
            play_song(current_index - 1 if current_index - 1 >= 1 else len(songs))

        elif cmd.startswith("set volume"):
            try:
                v = int(cmd.split()[2])
                if 0 <= v <= 100:
                    pygame.mixer.music.set_volume(v / 100)
                    print(f"Volume {v}%")
            except:
                print("Invalid command. Example: set volume 50")

        elif cmd == "list":
            list_songs()

        elif cmd == "repeat song":
            repeat_mode = "song"
            print("Repeat current song")

        elif cmd == "repeat album":
            repeat_mode = "album"
            print("Repeat album")

        elif cmd == "repeat off":
            repeat_mode = "none"
            print("Repeat off")

        elif cmd == "change_artist":
            pygame.mixer.music.stop()
            break

        elif cmd == "change_album":
            pygame.mixer.music.stop()
            current_dir_song = choose_dir("Select album:", artist_dir)
            songs = [f for f in os.listdir(current_dir_song) if f.lower().endswith(('.mp3', '.ogg'))]
            list_songs()
            current_song = current_index = None
            paused = False

        elif cmd == "exit":
            pygame.mixer.music.stop()
            exit()

        else:
            print("Unknown command.")
