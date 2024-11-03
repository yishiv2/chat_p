import tkinter
import socket
from tkinter import *
from threading import Thread

def receive():
    while True:
        try:
            msg = s.recv(1024).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except Exception as e:
            print("受信エラー:", e)
            break

def send():
    msg = my_msg.get()
    my_msg.set("")
    s.send(bytes(msg, "utf8"))
    if msg == "#quit":
        s.close()
        window.destroy()

def on_closing():
    my_msg.set("#quit")
    send()

def ask_username():
    username_window = Toplevel(window)
    username_window.title("ユーザー名の入力")
    username_label = Label(username_window, text="ユーザー名を入力してください:")
    username_label.pack()
    username_entry = Entry(username_window)
    username_entry.pack()

    def submit_username():
        username = username_entry.get()
        s.send(bytes(username, "utf8"))
        username_window.destroy()

    submit_button = Button(username_window, text="送信", command=submit_username)
    submit_button.pack()

    window.wait_window(username_window)  # ウィンドウが閉じるまで待機

# ウィンドウを作成
window = Tk()
window.title("Chat Room Application")
window.configure(bg="green")

# メッセージフレームを作成
message_frame = Frame(window, bg="red")
message_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

# メッセージ変数を作成
my_msg = StringVar()
my_msg.set("")

# スクロールバー
scrollbar = Scrollbar(message_frame)
scrollbar.pack(side=RIGHT, fill=Y)

# メッセージリストを作成
msg_list = Listbox(message_frame, height=15, width=100, bg="blue", yscrollcommand=scrollbar.set)
msg_list.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.config(command=msg_list.yview)

# メッセージ入力フィールドと送信ボタン
entry_field = Entry(window, textvariable=my_msg, fg='red')
entry_field.grid(row=1, column=0, sticky="ew")
send_button = Button(window, text="Send", font="Arial", fg="white", command=send)
send_button.grid(row=1, column=1)

# レスポンシブレイアウト設定
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# サーバー接続情報
host = "127.0.0.1"
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

# ユーザー名の入力
ask_username()

# メッセージ受信スレッドの開始
receive_thread = Thread(target=receive)
receive_thread.start()

# ウィンドウを閉じるイベント
window.protocol("WM_DELETE_WINDOW", on_closing)
mainloop()
