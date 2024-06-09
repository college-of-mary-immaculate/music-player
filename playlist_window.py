from playlist import ConcretePlaylist
from command import *

import tkinter as tk

class Add_Playlist(tk.Toplevel):
    def __init__(self, master, song_data:dict):
        super().__init__(master)
        self.song_data = song_data

        self.playlists = Load_JSON("playlist.json").execute()

        # Color varibles
        self.bg_color = "#660000"
        self.frame_color = "#6fa8dc"

        self.__configure_window()
        self.__add_frames()
        self.__add_labels()
        self.__add_entry()
        self.__add_buttons()

        #Config_WidgetSize(self.create_playlist_frame, 20, 3).execute()

    def __configure_window(self):
        self.title("Add to Playlist")
        #self.resizable(False, False)
        #self.geometry("350x500")
    
    def __add_frames(self):
        self.root_frame = tk.LabelFrame(self, text="Root Frame", bg=self.bg_color)
        self.root_frame.pack(expand=True)

        self.main_frame = tk.LabelFrame(self.root_frame, text="Main Frame",bg=self.bg_color)
        self.main_frame.pack(expand=True)

        self.create_playlist_frame = tk.LabelFrame(self.main_frame, text="Create laylist", bg= self.frame_color)
        self.create_playlist_frame.grid(column=0, row=0)

        self.add_playlist_frame = tk.LabelFrame(self.main_frame, text="Add Playlist", bg=self.frame_color)
        self.add_playlist_frame.grid(column=0, row=1)

    def __add_labels(self):
        self.create_playlist_lbl = tk.Label(self.create_playlist_frame, text="Create Playlist", bg=self.frame_color)
        self.create_playlist_lbl.grid(column=0, row=0)

    def __add_buttons(self):
        self.create_playlist = tk.Button(self.create_playlist_frame, text="Create Playlist", command=Create_Playlist(self.create_playlist_name_entry).execute())
        self.create_playlist.grid(column=0, row=2, sticky="ew")

        self.add_playlist_btn = tk.Button(self.add_playlist_frame, text="Add to Playlist", command=self.add_playlist)
        self.add_playlist_btn.grid(column=0, row=1, sticky="ew")

    def __add_entry(self):
        self.create_playlist_name_entry = tk.Entry(self.create_playlist_frame)
        self.create_playlist_name_entry.grid(column=0, row=1)

        self.add_playlist_name_entry = tk.Entry(self.add_playlist_frame)
        self.add_playlist_name_entry.grid(column=0, row=0, sticky="ew")

    def add_playlist(self):
        entry = self.add_playlist_name_entry.get()

        for playlist_name, playlist_data in self.playlists.items():
            if playlist_name.lower() == entry.lower():
                playlist_data["songs"].append(self.song_data["title"])
                Save_JSON(self.playlists, "playlist.json").execute()
                MsgBx_ShowInfo(f"Successfully added to {playlist_name}").execute()

    def destroy(self):
        super().destroy()
        if self.master:
            self.master.add_playlist_window = None