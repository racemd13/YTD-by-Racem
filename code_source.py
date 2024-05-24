from tkinter import ttk
from tkinter import Menu
import customtkinter as ctk
from pytube import YouTube
import threading
import pyperclip


def pop_menu(event):
    menu.tk_popup(event.x_root, event.y_root)

def copy():
    selected_text = app.focus_get().selection_get()
    pyperclip.copy(selected_text)

def cut():
    selected_text = app.focus_get().selection_get()
    pyperclip.copy(selected_text)
    app.focus_get().delete("sel.first", "sel.last")

def paste():
    clipboard_text = pyperclip.paste()
    app.focus_get().insert("insert", clipboard_text)

def startDownloadThread():
    threading.Thread(target=startDownload).start()

def title_fetch(ytLink):
    try:
        yt_title = YouTube(ytLink).title
        valid_link = ctk.CTkLabel(app, text="Title: " + yt_title, font=("Arial", 13, "bold"))
        valid_link.place(relx=0.5, rely=0.1, anchor='center')
    except:
        invalid_link= ctk.CTkLabel(app,text="Invalid Link", text_color="red", font=("Arial",13,"italic"))
        invalid_link.place(relx=0.5, rely=0.1, anchor='center')

def startDownload():
    ytLink = link.get()

    title_fetch(ytLink)

    try:
        resolution = resolution_var.get()
        folder = folderLink.get()

        if resolution == "highest":
            downloading_label.configure(text="downloading...")
            dwn = YouTube(ytLink).streams.get_highest_resolution()
            dwn.download(folder)
            downloading_label.destroy()
        elif resolution == "lowest":
            downloading_label.configure(text="downloading...")
            dwn = YouTube(ytLink).streams.get_lowest_resolution()
            dwn.download(folder)
            downloading_label.destroy()
        elif resolution == "audio":
            downloading_label.configure(text="downloading...")

            # Get audio streams and choose the one with the highest bitrate
            audio_streams = YouTube(ytLink).streams.filter(only_audio=True)
            best_audio = audio_streams.order_by('abr').desc().first()
            best_audio.download(folder)

            '''dwn = YouTube(ytLink).streams.get_audio_only()
            dwn.download(folder)'''
            downloading_label.destroy()
        else:
            downloading_label.configure(text="downloading...")
            dwn = YouTube(ytLink).streams.filter(res=resolution).first()
            dwn.download(folder)
            downloading_label.destroy()

    except Exception as e:
        print("An error occurred:", str(e))
    finish_label.configure(text="downloaded!", text_color="blue")


def browsing():
    directory = ctk.filedialog.askdirectory(title="Save Video")
    folderLink.delete(0, "end")
    folderLink.insert(0, directory)

#system settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#app frame
app = ctk.CTk()
app.geometry("600x300")
app.resizable(False, False)
app.title("Youtube Video Downloader")

#title
title = ctk.CTkLabel(app, text="INSERT A YOUTUBE LINK: ")
title.place(relx=0.02, rely=0.35, anchor="w")

#input link
link = ctk.CTkEntry(app, width=350, height=40)
link.place(relx=0.5, rely=0.46, anchor="center")

#finished downloading
finish_label = ctk.CTkLabel(app, text="")
finish_label.place(relx=0.5, rely=0.2, anchor='center')

#downloading label
downloading_label = ctk.CTkLabel(app, text="")
downloading_label.place(relx=0.5, rely=0.2, anchor='center')

#download button
download_button = ctk.CTkButton(app, text="Download", command=startDownloadThread)
download_button.place(relx=0.35, rely=0.8, anchor="center")

#combobox
resolutions = ["highest","1080p","720p","lowest","audio"]
resolution_var = ctk.StringVar()
resolution_combobox = ttk.Combobox(app, values=resolutions, textvariable=resolution_var)
resolution_combobox.place(relx=0.5, rely=0.69, anchor="center")
resolution_combobox.set("720p")

#folder link
folderLink = ctk.CTkEntry(app, width=350, height=20)
folderLink.place(relx=0.5, rely=0.6, anchor="center")

#browse button
browse = ctk.CTkButton(app, text="Browse", command=browsing)
browse.place(relx=0.6, rely=0.8, anchor="center")

# right click SECTION
menu = Menu(app, tearoff=0, bg="white", fg="black")

# options
menu.add_command(label="Copy", command=copy)
menu.add_command(label="Cut", command=cut)
menu.add_separator()
menu.add_command(label="Paste", command=paste)

# menu popping up
app.bind("<Button-3>", pop_menu)

app.mainloop()
