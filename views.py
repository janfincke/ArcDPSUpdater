from Tkinter import *

from updater import ArcDpsUpdater


class Window(Frame):
    def __init__(self, master=None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("ArcDPS Updater")
        self.pack(fill=BOTH, expand=1)

        quit_button = Button(self, text="Exit", command=self.exit_client, width=50)
        update_button = Button(self, text='Update and launch Guild Wars 2', width=50, command=self.launch_game)
        update_button.place(relx=0.5, rely=0.2, anchor=CENTER)
        quit_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    def exit_client(self):
        exit()

    def launch_game(self):
        updater = ArcDpsUpdater()
        updater.check_for_updates()
        self.exit_client()
