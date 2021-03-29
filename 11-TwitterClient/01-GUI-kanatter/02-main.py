from tkinter import *
from tkinter import ttk

def push_button():
    print(txt.get())

win = Tk()
win.title('test')

#エデットボックス作成
txt = StringVar()
edit = ttk.Entry(win, textvariable=txt) 
edit.grid(row=1,column=1)
edit.grid_configure(padx=5, pady=5)

#ボタン作成
button = ttk.Button(win, text='OK', command=push_button)
button.grid(row=2,column=2)
button.grid_configure(padx=5, pady=5)

win.mainloop()

print(txt.get())
