import tkinter as tk
from tkinter import ttk

root = tk.Tk()
style = ttk.Style()
style.theme_use('alt')

# list the options of the style
# (Argument should be an element of TScrollbar, eg. "thumb", "trough", ...)
print(style.element_options("Vertical.TScrollbar.trough"))

# configure the style
style.configure("Vertical.TScrollbar", gripcount=0, bd=0,
                background="Green", darkcolor="DarkGreen", lightcolor="LightGreen",
                troughcolor="gray", bordercolor="blue", arrowcolor="white")

hs = ttk.Scrollbar(root, orient="vertical")
hs.place(x=5, y=5, width=150)
hs.set(0.2,0.3)

root.mainloop()