from tkinter import *

root = Tk()
root.option_add('*font', ('FixedSys', 14))

# ペインドウィンドウ 1
pw1 = PanedWindow(root)
pw1.pack(expand = True, fill = BOTH)

# ラベル 1
a = Label(pw1, text = 'panedwindow\ntest1', bg = 'yellow')

# ペインドウィンドウ 2
pw2 = PanedWindow(pw1, orient = 'vertical')

# ラベル 2, 3
b = Label(pw2, text = 'panedwindow\ntest2', bg = 'cyan')
c = Label(pw2, text = 'panedwindow\ntest3', bg = 'pink')

# ペインドウィンドウに配置
pw1.add(a)
pw1.add(pw2)
pw2.add(b)
pw2.add(c)

root.mainloop()
