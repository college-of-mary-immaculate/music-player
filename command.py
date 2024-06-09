from abc import ABC, abstractmethod
from tinytag import TinyTag
from tkinter import messagebox

import os
import json
import random
import tkinter as tk

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

# Messaeboxes
class MsgBx_ShowInfo(Command):
    def __init__(self, message:str):
        self.__message = message

    def execute(self):
        return messagebox.showinfo(title="Show Info", message=self.__message)

class MsgBx_ShowWarning(Command):
    def __init__(self, message:str):
        self.__message = message

    def execute(self):
        return messagebox.showwarning(title="Show Warning", message=self.__message)

# Configure Widget Size
class Config_WidgetSize(Command):
    def __init__(self, frame, width_val, height_val) -> None:
        self.__frame = frame
        self.__width_val = width_val
        self.__height_val = height_val

    def execute(self):
        for widget in self.__frame.winfo_children():
            widget.config(width= self.__width_val, height= self.__height_val)

class Config_WidgetPadding(Command):
    def __init__(self, frame, padx_val, pady_val):
        self.__frame = frame
        self.__padx_val = padx_val
        self.__pady_val = pady_val

    def execute(self):
        for widget in self.__frame.winfo_children():
            widget.grid_configure(padx=self.__padx_val, pady=self.__pady_val)

class Config_WidgetFontSize(Command):
    def __init__(self, frame, font:str, size:int) -> None:
        self.__frame = frame
        self.__font = font
        self.__size = size

    def execute(self):
        for widget in self.__frame.winfo_children():
            widget.config(font=(self.__font, self.__size))

class Show_Frame(Command):
    def __init__(self, frame):
        self.__frame = frame

    def execute(self):
        self.__frame.tkraise()

class Hide_Frame(Command):
    def __init__(self, frame):
        self.__frame = frame

    def execute(self):
        self.__frame.lower()

class Get_Metadata(Command):
    def __init__(self, track):
        self.__track = track

    def execute(self):
        try:
            tag = TinyTag.get(self.__track)
            return tag
        except Exception as e:
            print("Error:", e)
            return None

class Get_Duration(Command):
    def __init__(self, track):
        self.__track = track

    def execute(self):
        try:
            tag = TinyTag.get(self.__track)
            duration_seconds = tag.duration
            minutes = int(duration_seconds // 60)
            seconds = int(duration_seconds % 60)
            duration_formatted = f"{minutes:02d}:{seconds:02d}"
            return duration_formatted
        
        except Exception as e:
            print("Error:", e)
            return None

class Get_Artist(Command):
    def __init__(self, track):
        self.__track = track

    def execute(self):
        try:
            tag = TinyTag.get(self.__track)
            return tag.artist
        
        except Exception as e:
            print("Error:", e)
            return None
        
class Get_Album(Command):
    def __init__(self, track):
        self.__track = track

    def execute(self):
        try:
            tag = TinyTag.get(self.__track)
            return tag.album
        
        except Exception as e:
            print("Error:", e)
            return None
        
class Get_Title(Command):
    def __init__(self, track):
        self.__track = track

    def execute(self):
        try:
            tag = TinyTag.get(self.__track)
            return tag.title
        
        except Exception as e:
            print("Error:", e)
            return None

class Get_Genre(Command):
    def __init__(self, track):
        self.__track = track

    def execute(self):
        try:
            tag = TinyTag.get(self.__track)
            if tag.genre:
                return tag.genre
        
        except Exception as e:
            print("Error:", e)
            return None
        
# Load the music and save to JSON
class Load_Save_to_JSON(Command):
    def execute(self):
        files = os.listdir("music")
        song_data = {}

        for file in files:
            song_path = os.path.join("music", file)
            title = Get_Title(song_path).execute()
            artist = Get_Artist(song_path).execute()
            album = Get_Album(song_path).execute()
            genre = Get_Genre(song_path).execute()
            duration = Get_Duration(song_path).execute()
            song_data.update({title:{
                "title": title,
                "artist": artist,
                "album": album,
                "duration": duration,
                "filename": file,
                "file_path": song_path,
                "play_counter": 0,
                "is_favorite": False,
                "genre": genre
            }})

        Save_JSON(song_data, "music_data.json").execute()
        return song_data
    
class Load_Dir(Command):
    def execute(self):
        files = os.listdir("music")
        song_data = {}

        for file in files:
            song_path = os.path.join("music", file)
            title = Get_Title(song_path).execute()
            artist = Get_Artist(song_path).execute()
            album = Get_Album(song_path).execute()
            genre = Get_Genre(song_path).execute()
            duration = Get_Duration(song_path).execute()
            song_data.update({title:{
                "title": title,
                "artist": artist,
                "album": album,
                "duration": duration,
                "filename": file,
                "file_path": song_path,
                "play_counter": 0,
                "is_favorite": False,
                "genre": genre,
            }})
        
        return song_data
    
# Save the changes in JSON
class Save_JSON(Command):
    def __init__(self, data, file_path):
        self.__data = data
        self.__file_path = file_path

    def execute(self):
        with open(self.__file_path, "w") as filewrite:
            json.dump(self.__data, filewrite, indent=4)

class Load_JSON(Command):
    def __init__(self, file_path):
        self.__file_path = file_path

    def execute(self):
        if os.path.exists(self.__file_path):
            with open(self.__file_path, "r") as fileread:
                return json.load(fileread)
        else:
            return {}

# Update the play_counter
class Add_Count(Command):
    def __init__(self, dict1:dict, dict2:dict, file_path:str):
        self.__dict1 = dict1
        self.__dict2 = dict2
        self.__file_path = file_path
        self.__music_data = self.__dict2

    def execute(self):
        title = self.__dict1["title"]

        for key, value in self.__dict2.items():
            if key == title:
                value["play_counter"] += 1
                Save_JSON(self.__music_data, self.__file_path).execute()

class Add_Count_Playist(Command):
    def __init__(self, dict1:dict, title:str, file_path:str):
        self.__dict1 = dict1
        self.__title = title
        self.__file_path = file_path

    def execute(self):
        for key, value in self.__dict1.items():
            if key == self.__title:
                value["play_count"] += 1
                Save_JSON(self.__dict1, self.__file_path).execute()
        
class Change_Favorite(Command):
    def __init__(self, dict1:dict, dict2:dict):
        self.__dict1 = dict1
        self.__dict2 = dict2

    def execute(self):
        title = self.__dict1["title"]

        for key, value in self.__dict2.items():
            if key == title:
                value["is_favorite"] = True
                Save_JSON(self.__dict2, "music_data.json").execute()

class Add_To_Favorites(Command):
    def __init__(self, song_data:dict, music_data:dict, listbox:tk.Listbox):
        self.__song_data = song_data
        self.__listbox = listbox
        self.__music_data = music_data

    def execute(self):
        if self.__song_data["title"] not in self.__listbox.get(0, tk.END):
            self.__listbox.insert(0, self.__song_data["title"])
            Change_Favorite(self.__song_data, self.__music_data).execute()
            MsgBx_ShowInfo("Successfully Added to favorites!").execute()
        else:
            MsgBx_ShowInfo("Song is already in favorites!").execute()

class Bubble_Sort(Command):
    def __init__(self, dict1:dict):
        self.__dict1 = dict1

    def execute(self):
        items = list(self.__dict1.items())
        length = len(items)

        for i in range(length):
            swapped = False
            for j in range(0, length-i-1):
                if items[j][1] < items[j+1][1]: 
                    items[j], items[j+1] = items[j+1], items[j]
                    swapped = True

            if not swapped:
                break

        return dict(items)
    
class Edit_Distance(Command):
    def __init__(self, str1:str, str2:str):
        self.__str1 = str1
        self.__str2 = str2

    def execute(self):
        len1 = len(self.__str1)
        len2 = len(self.__str2)

        array = [[0] * (len2 + 1) for _ in range(len1 + 1)]
        
        i = j = 0

        for i in range(len1 + 1):
            for j in range(len2 + 1):
                if i == 0:
                    array[i][j] = j
                elif j == 0:
                    array[i][j] = i
                elif self.__str1[i - 1] == self.__str2[j - 1]:
                    array[i][j] = array[i - 1][j - 1]
                else:
                    array[i][j] = min(array[i][j - 1], array[i - 1][j], array[i - 1][j - 1]) + 1
        
        return array[len1][len2]
    
class Make_Mood(Command):
    def __init__(self, mood:str, genres:list):
        self.__mood = mood
        self.__genres = genres
        self.__mood_songs = []
        self.genres_file = Load_JSON("genre.json").execute()

    def execute(self):
        for genre_title, genre_songs in self.genres_file.items():
            if genre_title in self.__genres:
                self.__mood_songs.extend(genre_songs)

        print(f"Not Shuffled {self.__mood_songs}")

        random.shuffle(self.__mood_songs)

        print(f"Shuffled {self.__mood_songs}")

        return self.__mood_songs