from tkinter import *


#rootウィンドウを作成
root = Tk()
root.option_add('*font', ('FixedSys', 14))
root.title("Kanatter(プロトタイプ)")        #rootウィンドウのタイトルを変える
root.geometry("400x500")                    #rootウィンドウの大きさを320x240に


# ペインドウィンドウの生成
pw = PanedWindow(root, orient = 'vertical', sashwidth = 4)
pw.pack(expand = True, fill = BOTH)

# ラベルの生成
a = Label(pw, bg = "white", text = "タイムライン表示部分")
b = Label(pw, text = 'panedwindow\ntest2', bg = 'yellow')
c = Label(pw, text = "ツイート投稿部分", bg = 'cyan')





# ペインドウィンドウに配置
pw.add(a)
pw.add(b)
pw.add(c)




root.mainloop()
