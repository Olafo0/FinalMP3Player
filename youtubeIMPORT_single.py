from tkinter import filedialog
from pydub import AudioSegment

import pydub
import tkinter as tk
import tkinter.filedialog
import webbrowser
import customtkinter

def run():
    master = tk.Tk()
    master.geometry("300x300")
    master.title("Import a youtube Playlist")
    frame = tk.Frame(master)


    #Importing the playlist function
    def Import_song_playlist():
        from pytube import YouTube
        import os
  
        # url input from user
        #yt = YouTube(str(input("Enter the URL of the video you want to download: \n>> ")))
        yt = YouTube(str(main_entry.get()))
  
        # extract only audio
        video = yt.streams.filter(only_audio=True).first()
  
        # check for destination to save file
        print("Enter the destination (leave blank for current directory)")
        DOWNLOAD_DIR = filedialog.askdirectory()

        # download the file
        out_file = video.download(output_path=DOWNLOAD_DIR)
        print(out_file)
        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        #new_format_audio = AudioSegment.from_file(file=out_file)
        #new_format_audio.export(new_file,format="mp3")
        #print(new_file)
        os.rename(out_file, new_file)
     
        #result of success
        print(yt.title + " has been successfully downloaded.")
        webbrowser.open('https://snapsave.io/en26')












    Label_1 = tk.Label(frame, text="Please enter the url and press Enter.", font=("arial",10))
    Label_1.pack()

    main_entry = tk.Entry(frame,)
    main_entry.pack()

    enterButton = tk.Button(frame, text="Enter",command=Import_song_playlist)
    enterButton.pack()





    frame.pack(expand=True)
    master.mainloop()
