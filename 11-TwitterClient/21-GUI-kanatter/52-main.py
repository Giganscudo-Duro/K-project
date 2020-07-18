from tkinter import *

root = Tk()
root.option_add('*font', ('FixedSys', 14))

# グローバル変数
la = []
var = []

# ペインドウィンドウ
pw = PanedWindow(root, orient = 'vertical', showhandle = True, sashwidth = 4)
pw.pack(expand = True, fill = BOTH)

# フレーム
f = Frame(pw)
pw.add(f)

# ラベルの表示切り替え
def change_label(n):
    def _change():
        if var[n].get():
            pw.add(la[n])
        else:
            pw.forget(la[n])
    return _change

# チェックボタン
for x in range(4):
    v = BooleanVar()
    v.set(True)
    var.append(v)
    Checkbutton(f, text = 'display label %d' % x,
                variable = v, command = change_label(x)).pack()

# ラベル
for x, y in enumerate(('white', 'yellow', 'cyan', 'pink')):
  a = Label(pw, text = 'panedwindow\ntest%d' % x, bg = y)
  la.append(a)
  pw.add(a)

root.mainloop()
