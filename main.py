from Tkinter import Tk

from views import Window

root = Tk()
# size of the window
root.geometry("400x100")
# make not resizeable
root.resizable(False, False)

app = Window(root)
root.mainloop()
