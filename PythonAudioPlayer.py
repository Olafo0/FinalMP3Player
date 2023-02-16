from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pygame import mixer
from mutagen.mp3 import MP3
from PIL import Image, ImageTk


import os
import time
import tkinter.ttk as ttk
import pygame
import youtubeIMPORT_single as yti
import tkinter as tk
import customtkinter


def main_program():

    # Window 
    root = tk.Tk()
    root.title("Requiem")
    #Main res 520x620
    root.geometry("520x620")
    root.configure(bg="#0f1a2b")
    root.resizable(False,False)


    if os.path.isfile("Save.txt"):
        with open("Save.txt","r") as f:
            tempApps = f.read()
            tempApps = tempApps.split(",")

            _Items = [x for x in tempApps if x.strip()]

    
       
    mixer.init()

    reapter_for_sb = 1000

    #Tab View

    tabview = customtkinter.CTkTabview(master=root, height=700, width=720,border_width=0)
    tabview.place(x=-5,y=-10)

    tabview.add("Player")
    tabview.add("PlayList")

 # TAB 1 
    def play_time_bar():
        current_time = pygame.mixer.music.get_pos() / 1000

        #song_slider_label.config(text=f"Slider: {int(song_slider.get())} and Song Pos: {int(current_time)}")

        #Converts time in a string format
        converted_current_time = time.strftime("%M:%S",time.gmtime(current_time))

        # Get the current song playing
        if playlist.get(ACTIVE):
            current_song = playlist.curselection()
            song = playlist.get(current_song)
            song_mutagen = MP3(song)
            #Get the length of the song
            global song_length
            song_length = song_mutagen.info.length
            # Change the format
            converted_song_length = time.strftime("%M:%S",time.gmtime(song_length))
       
            current_time +=1



            if int(song_slider.get()) == int(song_length):
                status_bar.config(text=f"Time Elapsed: {converted_song_length} ")

            elif paused:
                pass


            elif int(song_slider.get()) == int(current_time):
                #Slider not moved--
                # Update the slider
                slider_position = int(song_length)
                song_slider.config(to=slider_position, value=int(current_time))
            else:
                #Slider moved--
                # Update the slider
                slider_position = int(song_length)
                song_slider.configure(to=slider_position, value=int(song_slider.get()))
                # Convert to time foormat
                converted_current_time = time.strftime("%M:%S",time.gmtime(int(song_slider.get())))

                status_bar.config(text=f"Time Elapsed: {converted_current_time} of {converted_song_length} ")

                next_time = int(song_slider.get()) + 1 
                song_slider.config(value=next_time)

            #keeps the function updated
            status_bar.after(reapter_for_sb,play_time_bar)


    def add_many_songs():
        songs = filedialog.askopenfilenames(initialdir="H:\\T-Level\\Mp3AudioPlayer\\Music",title="Choose a song",filetypes=(("mp3 Files","*.mp3"),))

        for song in songs:
            playlist.insert(END,song)

        
    #Adds the song to the list -----
    #Import a single song to the Playlist
    def add_one_song():
        #name_rid = filedialog.askdirectory()
        song = filedialog.askopenfilename(initialdir="H:\\T-Level\\Mp3AudioPlayer\\Music",title="Choose a song",filetypes=(("mp3 Files","*.mp3"),))
        #song = song.replace(name_rid,"")
        print(song)
    
        #Adds the song to the list
        playlist.insert(END,song)


    # Plays the song
    def play_song():

        status_bar.config(text="")

        song_slider.config(value=0)

        status_bar.config(text="")


        music_name=playlist.get(ACTIVE)
        music_name = music_name.replace("\n","")
        #current_playing_song = playlist.get(ACTIVE)
        #current_playing_song = current_playing_song.replace("\n","")
        mixer.music.load(playlist.get(ACTIVE))
        mixer.music.play()
        music.config(text=music_name[0:-4])

        #Activate the play time bar
        play_time_bar()

        #update slider
        #slider_position = int(song_length)
        #song_slider.config(to=slider_position, value=1)


    global stopped
    stopped = False

    def stop():
        #Resets slider 

        status_bar.config(text="")

        song_slider.config(value=0)
        mixer.music.stop()
        playlist.selection_clear(ACTIVE)

        status_bar.config(text="")

        global stopped
        stopped = True


    #Paused is globalised so it can be assigned into a variable in the function
    global paused
    paused = False

    # Pause and Unpause the song
    def pause(is_paused):
        # We make paused global in this function so we can change it outside the function
        global paused
        paused = is_paused

        # If the variable is true the song is unpaused
        if paused == True:
            #Unpause
            mixer.music.unpause()
            paused = False
            global Paused_Label
            pause_music_button.configure(image=pause_button)
            

        # If the variable is false the song is paused
        else:
            mixer.music.pause()
            paused = True
            pause_music_button.configure(image=unpause_button)


        # Remove songs
    def remove_song():
        stop()
        playlist.delete(ANCHOR)
        mixer.music.stop()

    def remove_all_songs():
        stop()
        playlist.delete(0,END)
        mixer.music.stop()



    def slide(x):
        try:
            #song_slider_label.config(text=f"{int(song_slider.get())} of {int(song_length)}")
            song = playlist.get(ACTIVE)
            # Change the name 
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=0, start=int(song_slider.get()))
        except :
            pass

    def volume(x):
        pygame.mixer.music.set_volume(volume_slider.get())


    def forwardSong():

        status_bar.config(text="")

        song_slider.config(value=0)

        status_bar.config(text="")

        #Current song played
        next_one = playlist.curselection()
        next_one = next_one[0]+1
        song = playlist.get(next_one)

        #Plays the next song
        try:
            mixer.music.load(song)
            mixer.music.play()
        except FileNotFoundError:
            pass
    
        #Updates the bar in the playlist
        playlist.selection_clear(0, END)
        #Moves to the next song
        playlist.activate(next_one)
        playlist.select_set(next_one, last=None)

        music_name=playlist.get(ACTIVE)

        music_name = music_name.replace("H:/T-Level/Mp3AudioPlayer/Music/SnapSave.io -","")
        music.config(text=music_name[0:-4])


    def PreviousSong():

        status_bar.config(text="")

        song_slider.config(value=0)

        status_bar.config(text="")

        #Current song played
        next_one = playlist.curselection()
        next_one = next_one[0]-1
        song = playlist.get(next_one)

        #Plays the next song
        mixer.music.load(song)
        mixer.music.play()
    
        #Updates the bar in the playlist
        playlist.selection_clear(0, END)
        #Moves to the next song
        playlist.activate(next_one)
        playlist.select_set(next_one, last=None)

        music_name=playlist.get(ACTIVE)
        music.config(text=music_name[0:-4])


    def Import_Youtube_Playlist():
        yti.run()

    #Icon
    image_icon = tk.PhotoImage(file="GUI/WolfGangIcon.png")

    # Little window logo
    root.iconphoto(False,image_icon)


    #Main logo (Top LEFT)
    #Logo_main = tk.Label(image=image_icon).place(x=0,y=0)


    #Updated background  (re-adding)
    background_image_main = tk.PhotoImage(file="GUI/thumbnail_Backb.PNG")
    background_image_main_label = tk.Label(master=tabview.tab("Player"),image=background_image_main)
    background_image_main_label.place(x=-10,y=-10)
    #background_image_main_label.lower()


    #Buttons 
    play_button = ImageTk.PhotoImage(Image.open("GUI/Play_Button.png").resize((70,70)))
    play_music_button = customtkinter.CTkButton(master=tabview.tab("Player"),image=play_button,command=play_song,text="",fg_color="black",bg_color="black", width=30, height=30, compound="top",hover=False)
    play_music_button.place(x=280,y=430)

    
    unpause_button = ImageTk.PhotoImage(Image.open("GUI/Unpause_Button.png").resize((70,70)))
    pause_button = ImageTk.PhotoImage(Image.open("GUI/Pause_Button.png").resize((70,70)))

    pause_music_button = customtkinter.CTkButton(master=tabview.tab("Player"),image=pause_button,command=lambda: pause(paused),text="",fg_color="black",bg_color="black",width=30,height=30,compound="top",hover=False)
    pause_music_button.place(x=360,y=430)
    #360


    Forward_button = ImageTk.PhotoImage(Image.open("GUI/Forward_Button.png").resize((60,60)))
    forward_music_button = customtkinter.CTkButton(master=tabview.tab("Player"),image=Forward_button,command=forwardSong,text="",fg_color="black",bg_color="black",width=30,height=30,compound="top",hover=False).place(x=440,y=435)

    Previous_button = ImageTk.PhotoImage(Image.open("GUI/Backward_buton.png").resize((60,60)))
    previous_music_button = customtkinter.CTkButton(master=tabview.tab("Player"), image=Previous_button,command=PreviousSong,text="",fg_color="black",bg_color="black", width=30, height=30, compound="top",hover=False).place(x=205, y=435)


    #Music viewer
    music_frame = tk.Frame(master=tabview.tab("Player"), bd=1, relief=RIDGE)
    music_frame.place(x=0,y=50,width=175,height=500)


    #Import Button/cascade

    # Create a menu casecade -----
    my_menu = Menu(root)
    root.config(menu=my_menu)

    # Importing a song
    add_song_menu = Menu(my_menu)
    my_menu.add_cascade(label="IMPORT A SONG", menu=add_song_menu)
    add_song_menu.add_command(label="Import one song to Playlist", command=add_one_song)
    add_song_menu.add_command(label="Import many songs to Playlist", command=add_many_songs)
    add_song_menu.add_command(label="Import a youtube playlist", command=Import_Youtube_Playlist)

    #Deleting a song
    remove_song_menu = Menu(my_menu)
    my_menu.add_cascade(label="REMOVE A SONG", menu=remove_song_menu)
    remove_song_menu.add_command(label="Remove a song from the playlist",command=remove_song)
    remove_song_menu.add_command(label="Remove all songs from the playlist",command=remove_all_songs)

    #Import youtube playlist
    youtubeImport_Cascade = Menu(my_menu)
    my_menu.add_cascade


    #Music Label (Displays what song is playing)
    music = tk.Label(master=tabview.tab("Player"), text="",font=("arial",9),fg="black",bg="#e2e2e3")
    music.place(x=270,y=250,anchor="center")



    # music_frame viwers scroll code
    scroll = tk.Scrollbar(music_frame)
    playlist = tk.Listbox(music_frame,width=100,font=("arial",10),bg="black",fg="grey",selectbackground="grey",
                       cursor="hand2",bd=0,yscrollcommand=scroll.set)
    ##333333
    scroll.config(command=playlist.yview)
    scroll.pack(side=RIGHT, fill=Y)
    playlist.pack(side=LEFT,fill=BOTH)



    #Status bar
    status_bar = Label(master=tabview.tab("Player"), text="",font=("arial",10),fg="black",bg="#e2e2e3",bd=1, relief=GROOVE, anchor=CENTER)
    status_bar.pack(fill=X,side=BOTTOM,ipady=2)
    status_bar.place(x=300,y=350)


    #Position Slider
    song_slider = ttk.Scale(master=tabview.tab("Player"), from_=0, to=100,orient=HORIZONTAL, value=0, command=slide,length=200)
    #song_slider = TickScale(root, from_=0, to=100,orient="horizontal",value=0,command=slide,length=200, digits=intVar)
    song_slider.place(x=270,y=375)


    volume_frame = LabelFrame(master=tabview.tab("Player"), text="- | Volume | +")
    volume_frame.place(x=270,y=100)

    volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=HORIZONTAL, value=1, command=volume,length=200)
    volume_slider.pack(pady=10)


    #Save your playlist into a file.
    def save_playlist():
        stuff = []

        x = playlist.size()
        file=open("Test.txt","a")
        for i in range(0,x):
            temp = playlist.get(i)
            stuff.append(temp)
        for i in range(0,x):
            sn = stuff[i]+"\n"
            file.write(sn)
  
        file.close()

        file =open("Test.txt","r")
        file.readline()

        while True:
            x = x+1
            content_in_file = file.readline(x)
            if content_in_file == "":
                break
                file.close()
            else:
                pass
        file.close()
  

    pl_in_lib = []

    #Insert a file in the selection listbox
    def insert_file_to_listbox():
        pl = filedialog.askopenfilenames(title="Choose your playlist",filetypes=(("","*.txt"),))
        selection_listbox.insert(END,pl)
        global _Items
        _Items = []
        x = selection_listbox.size()

        for i in range(0,x):
            temp = selection_listbox.get(i)
            print(temp)
            temp2 = str(temp)
            #Gets rid of the tuple which was causing errors
            temp3 = temp2.replace("(","").replace(")","").replace("'","")
            _Items.append(temp3)
            print(_Items,"List")


        # Appends to data in the selection Listbox to a file
        with open("Save.txt","w") as f:
            for _item in _Items:
                f.write(_item)
                f.close()
           
    #Deletes whatever is selected 
    def delete_file_from_listbox():


        # Deletes the playlist from the textfile so it doesn't appear when you boot up the program
        Name_of_Playlist = selection_listbox.get(ACTIVE)
        S_Name_of_Playlist = str(Name_of_Playlist)
        temp3 = S_Name_of_Playlist.replace("(","").replace(")","").replace("'","")


        file = open("Save.txt","r")
        the_line = file.read()
        file.close()
        print(the_line)

        the_line = the_line.replace(temp3 + ",","")
        print(Name_of_Playlist)
        print(the_line)

        file = open("Save.txt","w")
        file.write(the_line)
        file.close()

        selection_listbox.delete(ACTIVE)

        #for content in range(playlist.size):
            #stuff.append(playlist[content])

       #print(stuff)

    
    def load_playlist():
        playlist.delete(0,END)
        TempFlag = True
        while TempFlag:

            p_l_i_f = []


            x = selection_listbox.get(ACTIVE)
            x = str(x)
            temp = x.replace("(","").replace(")","").replace("'","").replace(",","")
            TempFlag = False
            filee = open(f"{temp}","r")
            while True:
                content_in_text = filee.readline()
                content_in_text = content_in_text.replace("\n","")
                if content_in_text == "":
                    filee.close()
                    break
                else:
                   print(content_in_text)
                   playlist.insert(END, content_in_text)

            else:
                print("no")
                break
           

    #Updated background  (re-adding)
    background_image_playlist = tk.PhotoImage(file="GUI/youtube_background.PNG")
    background_image_playlist_label = tk.Label(master=tabview.tab("PlayList"),image=background_image_playlist)
    background_image_playlist_label.place(x=-10,y=-10)
    #background_image_main_label.lower()



    #Buttons
    save_playlist_button = customtkinter.CTkButton(master=tabview.tab("PlayList"),text="Save Playlist from player ",corner_radius=6,border_width=4,border_color="#3E7FE9",fg_color="#4282E5",font=("arial",10),command=save_playlist)
    save_playlist_button.place(x=325,y=100)

    delete_playlist_button = customtkinter.CTkButton(master=tabview.tab("PlayList"),text="Delete selected Playlist",corner_radius=6,border_width=4,border_color="red",fg_color="red",hover_color="#FF7E82",font=("arial",10),command=delete_file_from_listbox)
    delete_playlist_button.place(x=325,y=160)

    insert_playlist_button = customtkinter.CTkButton(master=tabview.tab("PlayList"),text="Insert your playlist",corner_radius=6,border_width=4,border_color="#3E7FE9",fg_color="#4282E5",font=("arial",10),command=insert_file_to_listbox)
    insert_playlist_button.place(x=325,y=130)


    load_playlist_button = customtkinter.CTkButton(master=tabview.tab("PlayList"),text="Load your playlist", corner_radius=6, border_width=4,border_color="#3E7FE9",fg_color="#4282E5",bg_color="#3E7FE9",font=("arial",20),command=load_playlist)
    load_playlist_button.place(x=30,y=10)

    #Label
    insert_label = customtkinter.CTkLabel(master=tabview.tab("PlayList"),text="NOTE: Make sure your songs are in a textfile",font=("arial",10),fg_color="transparent")
    insert_label.place(x=280,y=220,anchor="w")
    insert_label2 = customtkinter.CTkLabel(master=tabview.tab("PlayList"),text="-If you want your playlist to be in a textfile import",font=("arial",9),fg_color="transparent")
    insert_label2.place(x=280,y=250,anchor="w")
    insert_label5 = customtkinter.CTkLabel(master=tabview.tab("PlayList"),text="it (in player) and save it by using the",font=("arial",9),fg_color="transparent")
    insert_label5.place(x=280,y=280,anchor="w")
    insert_label3 = customtkinter.CTkLabel(master=tabview.tab("PlayList"),text="this makes your playlist",font=("arial",9),fg_color="transparent")
    insert_label3.place(x=280,y=310,anchor="w")
    insert_label4 = customtkinter.CTkLabel(master=tabview.tab("PlayList"),text="automatically into a texfile and compatible",font=("arial",9))
    insert_label4.place(x=280,y=340,anchor="w")












    #ListBox
        #Music viewer
    music_frame2 = tk.Frame(master=tabview.tab("PlayList"), bd=1, relief=RIDGE)
    music_frame2.place(x=0,y=50,width=250,height=500)


    #Selection Listbox
    scroll2 = tk.Scrollbar(music_frame2)
    selection_listbox = tk.Listbox(music_frame2,width=100,font=("arial",10),bg="black",fg="grey",selectbackground="grey",
                       cursor="hand2",bd=0,yscrollcommand=scroll.set)


    #
    scroll2.config(command=playlist.yview)
    scroll2.pack(side=RIGHT, fill=Y)
    selection_listbox.pack(side=LEFT,fill=BOTH)



    for _Item in _Items:
        selection_listbox.insert(END, _Item)

   
    root.mainloop()


main_program()